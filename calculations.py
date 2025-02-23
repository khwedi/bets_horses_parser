async def calculate_net_gain(bk1_cf, bk1_stake_amount, ew, place):
    bk1_cf = float(bk1_cf)
    place = int(place)
    bk1_stake_amount = float(bk1_stake_amount)
    bk1_winloss = bk1_stake_amount * (-1)
    status = 'LOSS'

    if ew is None:
        if place == 1:
            bk1_winloss = bk1_stake_amount * bk1_cf - bk1_stake_amount
            status = 'WIN'
    else:
        ew_split = ew.split('_')
        denominator_ew = eval(ew_split[0])
        number_of_prizes = int(ew_split[1])

        if 1 <= place <= number_of_prizes:
            half_bk1_stake_amount = bk1_stake_amount / 2
            kef_placed = (bk1_cf - 1) * denominator_ew + 1
            second_part_bet = half_bk1_stake_amount * kef_placed - half_bk1_stake_amount

            first_part_bet = 0
            if place == 1:
                first_part_bet = half_bk1_stake_amount * bk1_cf - half_bk1_stake_amount
                status = 'WIN'
            elif place <= number_of_prizes:
                first_part_bet = half_bk1_stake_amount * (-1)
                status = 'PLACED'

            bk1_winloss = first_part_bet + second_part_bet

    return bk1_winloss, status
