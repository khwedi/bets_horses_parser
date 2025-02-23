class Bet:
    def __init__(self, stake_timestamp, status, sport, country, location,
                 bk1_bet, bk1_stake_amount, bk1_winloss, bk1_cf, ew, id):
        self.id = id
        self.stake_timestamp = stake_timestamp
        self.status = status
        self.sport = sport
        self.country = country
        self.location = location
        self.bk1_bet = bk1_bet.title()
        self.bk1_stake_amount = bk1_stake_amount
        self.bk1_winloss = bk1_winloss
        self.bk1_cf = bk1_cf
        self.ew = ew
