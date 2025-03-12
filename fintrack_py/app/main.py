from functions_app import get_track_option, get_ticket_df
from queries import insert_launch
from classification import get_classification


def main():
    get_track_option()

    dict_classification = get_classification()

    dict_nfe_sc = get_ticket_df(dict_classification)

    insert_launch(dict_nfe_sc)


if __name__ == "__main__":
    main()
