#!/usr/bin/env python

"""
Fill the "player_prediction" table with score predictions
Usage:
python fill_predictedscore_table.py --weeks_ahead <nweeks>
Generates a "tag" string which is stored so it can later be used by team-optimizers to
get consistent sets of predictions from the database.
"""
import pickle
import pkg_resources
from uuid import uuid4

from multiprocessing import Process, Queue
import argparse

from airsenal.framework.bpl_interface import get_fitted_team_model
from airsenal.framework.utils import (
    list_players,
    NEXT_GAMEWEEK,
    CURRENT_SEASON,
    get_top_predicted_points,
)

from airsenal.framework.prediction_utils import (
    calc_predicted_points_for_player,
    calc_predicted_points_for_pos
)

from airsenal.framework.schema import session_scope


def calc_predicted_points_for_pos(
    pos,
    gw_range,
    team_model,
    player_model,
    season,
    tag,
    session,
    df_bonus,
    df_saves,
    df_cards,
):
    """
    Calculate points predictions for all players in a given position and
    put into the DB
    """
    predictions = {}
    df_player = None
    if pos != "GK":  # don't calculate attacking points for keepers.
        df_player = get_fitted_player_model(player_model, pos, season, session)
    for player in list_players(position=pos, dbsession=session):
        predictions[player.player_id] = calc_predicted_points(
            player,
            team_model,
            df_player,
            season,
            tag,
            session,
            df_bonus,
            df_saves,
            df_cards,
            gw_range,
        )

    return predictions


def allocate_predictions(
    queue,
    gw_range,
    team_model,
    player_model,
    season,
    tag,
    session,
    df_bonus,
    df_saves,
    df_cards,
):
    """
    Take positions off the queue and call function to calculate predictions
    """
    while True:
        pos = queue.get()
        if pos == "DONE":
            print("Finished processing {}".format(pos))
            break
        predictions = calc_predicted_points_for_pos(
            pos,
            gw_range,
            team_model,
            player_model,
            season,
            tag,
            session,
            df_bonus,
            df_saves,
            df_cards,
        )
        for k, v in predictions.items():
            for playerprediction in v:
                session.add(playerprediction)
        session.commit()
        print("Finished adding predictions to db for {}".format(pos))


def calc_all_predicted_points(
    gw_range,
    season,
    tag,
    session,
    num_thread=4,
    include_bonus=True,
    include_cards=True,
    include_saves=True,
):
    """
    Do the full prediction for players.
    """
    model_team = get_fitted_team_model(season, session, gameweek=min(gw_range))

    model_file = pkg_resources.resource_filename(
        "airsenal", "stan_model/player_forecasts.pkl"
    )
    with open(model_file, "rb") as f:
        model_player = pickle.load(f)

    if include_bonus:
        df_bonus = fit_bonus_points(gameweek=gw_range[0], season=season)
    else:
        df_bonus = None
    if include_saves:
        df_saves = fit_save_points(gameweek=gw_range[0], season=season)
    else:
        df_saves = None
    if include_cards:
        df_cards = fit_card_points(gameweek=gw_range[0], season=season)
    else:
        df_cards = None

    all_predictions = {}
    print("Num thread is {}".format(num_thread))
    if num_thread:
        queue = Queue()
        procs = []
        for i in range(num_thread):
            processor = Process(
                target=allocate_predictions,
                args=(
                    queue,
                    gw_range,
                    model_team,
                    model_player,
                    season,
                    tag,
                    session,
                    df_bonus,
                    df_saves,
                    df_cards,
                ),
            )
            processor.daemon = True
            processor.start()
            procs.append(processor)

        for pos in ["GK", "DEF", "MID", "FWD"]:
            queue.put(pos)
        for i in range(num_thread):
            queue.put("DONE")

        for i, p in enumerate(procs):
            p.join()
    else:
        # single threaded
        for pos in ["GK", "DEF", "MID", "FWD"]:
            predictions = calc_predicted_points_for_pos(
                pos,
                gw_range,
                model_team,
                model_player,
                season,
                tag,
                session,
                df_bonus,
                df_saves,
                df_cards,
            )
            for k, v in predictions.items():
                for playerprediction in v:
                    session.add(playerprediction)
        session.commit()
        print("Finished adding predictions to db for {}".format(pos))


def make_predictedscore_table(
    session,
    gw_range=None,
    season=CURRENT_SEASON,
    num_thread=4,
    include_bonus=True,
    include_cards=True,
    include_saves=True,
    tag_prefix=None,
    dbsession=None
):
    tag = tag_prefix if tag_prefix else ""
    tag += str(uuid4())
    if not gw_range:
        gw_range = list(range(NEXT_GAMEWEEK, NEXT_GAMEWEEK + 3))
    calc_all_predicted_points(
        gw_range,
        season,
        include_bonus=include_bonus,
        include_cards=include_cards,
        include_saves=include_saves,
        num_thread=num_thread,
        tag=tag,
        dbsession=dbsession
    )
    return tag


def main():
    """
    fill the player_prediction db table
    """
    parser = argparse.ArgumentParser(description="fill player predictions")
    parser.add_argument("--weeks_ahead", help="how many weeks ahead to fill", type=int)
    parser.add_argument("--gameweek_start", help="first gameweek to look at", type=int)
    parser.add_argument("--gameweek_end", help="last gameweek to look at", type=int)
    parser.add_argument("--ep_filename", help="csv filename for FPL expected points")
    parser.add_argument(
        "--season", help="season, in format e.g. '1819'", default=CURRENT_SEASON
    )
    parser.add_argument(
        "--num_thread", help="number of threads to parallelise over", type=int
    )
    parser.add_argument(
        "--no_bonus",
        help="don't include bonus points",
        action="store_true",
    )
    parser.add_argument(
        "--no_cards",
        help="don't include points lost to yellow and red cards",
        action="store_true",
    )
    parser.add_argument(
        "--no_saves",
        help="don't include save points for goalkeepers",
        action="store_true",
    )

    args = parser.parse_args()
    if args.weeks_ahead and (args.gameweek_start or args.gameweek_end):
        print("Please specify either gameweek_start and gameweek_end, OR weeks_ahead")
        raise RuntimeError("Inconsistent arguments")
    if args.weeks_ahead and not args.season == CURRENT_SEASON:
        print("For past seasons, please specify gameweek_start and gameweek_end")
        raise RuntimeError("Inconsistent arguments")
    if args.weeks_ahead:
        gw_range = list(range(NEXT_GAMEWEEK, NEXT_GAMEWEEK + args.weeks_ahead))
    elif args.gameweek_start and args.gameweek_end:
        gw_range = list(range(args.gameweek_start, args.gameweek_end))
    elif args.gameweek_start:  # by default go three weeks ahead
        gw_range = list(range(args.gameweek_start, args.gameweek_start + 3))
    else:
        gw_range = list(range(NEXT_GAMEWEEK, NEXT_GAMEWEEK + 3))
    num_thread = args.num_thread if args.num_thread else None
    include_bonus = not args.no_bonus
    include_cards = not args.no_cards
    include_saves = not args.no_saves

    with session_scope() as session:
        tag = make_predictedscore_table(
            session,
            gw_range=gw_range,
            season=args.season,
            num_thread=num_thread,
            include_bonus=include_bonus,
            include_cards=include_cards,
            include_saves=include_saves,
        )

        # print players with top predicted points
        get_top_predicted_points(
            gameweek=gw_range,
            tag=tag,
            season=args.season,
            dbsession=session,
            per_position=True,
            n_players=5,
        )
