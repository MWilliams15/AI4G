class BestWorst(object):

    def update(self, gameinfo):
        if gameinfo.my_fleets:
            return

        # check if we should attack
        if gameinfo.my_planets and gameinfo.not_my_planets:
            # select the best destination
            dest = min(gameinfo.not_my_planets.values(), key=lambda p: p.num_ships)

            # select best source
            src = max(gameinfo.my_planets.values(), key=lambda p: p.num_ships)

            # launch new fleet if there's enough ships
            if src.num_ships > 10:
                gameinfo.planet_order(src, dest, int(src.num_ships * 0.75))
