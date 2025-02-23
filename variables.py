class Variables:
    def __init__(self) -> object:
        self.url = 'https://betsapi.com'
        self.concept_class_name = 'fc-button fc-cta-consent fc-primary-button'
        self.cookies_class_name = 'btn btn-light float-right'

        self.login_class_name = 'btn btn-sm btn-outline-primary' #'nav-item d-none d-md-flex'
        self.login_with_google_class_name = 'btn btn-block btn-google'
        self.google_account_continue_class_name = 'VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b'
        self.have_logged_class_name = 'avatar'

        self.input_login_name = 'identifier'
        self.input_password_name = 'Passwd'
        self.gmail_login = 'khwedi.ananieva@gmail.com'
        self.gmail_password = 'Tomcruiselovegarfild123'

        self.upload_script = """select
                                pb.id,
                                pb.stake_timestamp,
                                pb.status,
                                pb.sport,
                                SUBSTRING_INDEX(pb.bk1_event, '.', 1) as country,
                                TRIM(SUBSTRING_INDEX(pb.bk1_event, '.', -1)) as location,
                                pb.bk1_bet,
                                pb.bk1_stake_amount,
                                pb.bk1_winloss,
                                pb.bk1_cf,
                                pb.ew
                            from sharp.placed_bets pb
                            where 1=1
                                and pb.sport = 'horses'
                                and pb.status in ('STAKED','NO_RESULT')
                                and pb.stake_timestamp >= current_date - interval 2 day
                            LIMIT 10
                            """
        self.updata_script = """UPDATE sharp.placed_bets
                                set status = %s, bk1_winloss = %s
                                where id = %s"""

        self.cookies_file_path = r'C:\Users\diana\PycharmProjects\BetsParser\cookies.txt'
        self.adblock_path = r'C:\Users\diana\PycharmProjects\BetsParser\AdBlockChrome.crx'
        self.results_block_path = "//a[@href='/e/']"

        # self.horse_racing_path = "//a[@href='/c/horse-racing/']"
        # self.advert_banner_name = 'ad_iframe'
        # self.close_banner_button_id = 'dismiss-button'
        # self.search_name = 'q'
        # self.google_account_class_name = 'aZvCDf oqdnae W7Aapd zpCp3 SmR8'

        # self.upload_script = """select
        #                         pb.id,
        #                         pb.stake_timestamp,
        #                         pb.status,
        #                         pb.sport,
        #                         SUBSTRING_INDEX(pb.bk1_event, '.', 1) as country,
        #                         TRIM(SUBSTRING_INDEX(pb.bk1_event, '.', -1)) as location,
        #                         pb.bk1_bet,
        #                         pb.bk1_stake_amount,
        #                         pb.bk1_winloss,
        #                         pb.bk1_cf,
        #                         pb.ew
        #                     from sharp.placed_bets pb
        #                     where 1=1
        #                         and pb.sport = 'horses'
        #                         and pb.bk1_bet = 'A Nod To Getaway'"""