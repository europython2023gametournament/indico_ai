# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from collections import defaultdict
import math

# This is your team name
CREATOR = "indico"


# This is the AI bot that will be instantiated for the competition
class PlayerAi:
    def __init__(self):
        self.team = CREATOR  # Mandatory attribute

        # Record the previous positions of all my vehicles
        self.previous_positions = {}
        # Record the number of tanks and ships I have at each base
        self.ntanks = {}
        self.nships = {}
        self.njets = {}
        self.defenders = defaultdict(dict)

    def run(self, t: float, dt: float, info: dict, game_map: np.ndarray):
        """
        This is the main function that will be called by the game engine.

        Parameters
        ----------
        t : float
            The current time in seconds.
        dt : float
            The time step in seconds.
        info : dict
            A dictionary containing all the information about the game.
            The structure is as follows:
            {
                "team_name_1": {
                    "bases": [base_1, base_2, ...],
                    "tanks": [tank_1, tank_2, ...],
                    "ships": [ship_1, ship_2, ...],
                    "jets": [jet_1, jet_2, ...],
                },
                "team_name_2": {
                    ...
                },
                ...
            }
        game_map : np.ndarray
            A 2D numpy array containing the game map.
            1 means land, 0 means water, -1 means no info.
        """

        # Get information about my team
        myinfo = info[self.team]

        # Controlling my bases =================================================

        # Description of information available on bases:
        #
        # This is read-only information that all the bases (enemy and your own) have.
        # We define base = info[team_name_1]["bases"][0]. Then:
        #
        # base.x (float): the x position of the base
        # base.y (float): the y position of the base
        # base.position (np.ndarray): the (x, y) position as a numpy array
        # base.team (str): the name of the team the base belongs to, e.g. ‘John’
        # base.number (int): the player number
        # base.mines (int): the number of mines inside the base
        # base.crystal (int): the amount of crystal the base has in stock
        #     (crystal is per base, not shared globally)
        # base.uid (str): unique id for the base
        #
        # Description of base methods:
        #
        # If the base is your own, the object will also have the following methods:
        #
        # base.cost("mine"): get the cost of an object.
        #     Possible types are: "mine", "tank", "ship", "jet"
        # base.build_mine(): build a mine
        # base.build_tank(): build a tank
        # base.build_ship(): build a ship
        # base.build_jet(): build a jet

        # Iterate through all my bases (vehicles belong to bases)
        # for base in myinfo["bases"]:
        #     # If this is a new base, initialize the tank & ship counters
        #     if base.uid not in self.ntanks:
        #         self.ntanks[base.uid] = 0
        #     if base.uid not in self.nships:
        #         self.nships[base.uid] = 0
        #     # Firstly, each base should build a mine if it has less than 3 mines
        #     if base.mines < 3:
        #         if base.crystal > base.cost("mine"):
        #             base.build_mine()
        #     # Secondly, each base should build a tank if it has less than 5 tanks
        #     elif base.crystal > base.cost("tank") and self.ntanks[base.uid] < 5:
        #         # build_tank() returns the uid of the tank that was built
        #         tank_uid = base.build_tank(heading=360 * np.random.random())
        #         # Add 1 to the tank counter for this base
        #         self.ntanks[base.uid] += 1
        #     # Thirdly, each base should build a ship if it has less than 3 ships
        #     elif base.crystal > base.cost("ship") and self.nships[base.uid] < 3:
        #         # build_ship() returns the uid of the ship that was built
        #         ship_uid = base.build_ship(heading=360 * np.random.random())
        #         # Add 1 to the ship counter for this base
        #         self.nships[base.uid] += 1
        #     # If everything else is satisfied, build a jet
        #     elif base.crystal > base.cost("jet"):
        #         # build_jet() returns the uid of the jet that was built
        #         jet_uid = base.build_jet(heading=360 * np.random.random())

        for base in myinfo["bases"]:
            # If this is a new base, initialize the tank & ship counters
            if base.uid not in self.ntanks:
                self.ntanks[base.uid] = 0
            if base.uid not in self.nships:
                self.nships[base.uid] = 0
            if base.uid not in self.njets:
                self.njets[base.uid] = 0
            # Firstly, each base should build a mine if it has less than 3 mines
            if base.mines < 3:
                if base.crystal > base.cost("mine"):
                    base.build_mine()
            # Secondly, each base should build a tank if it has less than 5 tanks

            nt = self.ntanks[base.uid]
            ns = self.nships[base.uid]
            nj = self.njets[base.uid]

            if ns < 2:
                if base.crystal > base.cost("ship"):
                    base.build_ship(heading=360 * np.random.random())
                    self.nships[base.uid] += 1
            elif nt < 2:
                if base.crystal > base.cost("tank"):
                    base.build_tank(heading=360 * np.random.random())
                    self.ntanks[base.uid] += 1
            elif nj < 1:
                base.build_jet(heading=360 * np.random.random())
                self.njets[base.uid] += 1
            elif nt < 5:
                if base.crystal > base.cost("tank"):
                    base.build_tank(heading=360 * np.random.random())
                    self.ntanks[base.uid] += 1
            elif ns < 4:
                if base.crystal > base.cost("ship"):
                    base.build_ship(heading=360 * np.random.random())
                    self.nships[base.uid] += 1
            elif base.crystal > base.cost("jet"):
                # build_jet() returns the uid of the jet that was built
                base.build_jet(heading=360 * np.random.random())
                self.njets[base.uid] += 1

            # elif base.crystal > base.cost("ship") and self.nships[base.uid] < 10:
            #     # build_ship() returns the uid of the ship that was built
            #     base.build_ship(heading=360 * np.random.random())
            #     # Add 1 to the ship counter for this base
            #     self.nships[base.uid] += 1
            # elif base.crystal > base.cost("tank") and self.ntanks[base.uid] < 10:
            #     base.build_tank(heading=360 * np.random.random())
            #     self.ntanks[base.uid] += 1
            # # Thirdly, each base should build a ship if it has less than 3 ships
            # # If everything else is satisfied, build a jet
            # elif base.crystal > base.cost("jet"):
            #     # build_jet() returns the uid of the jet that was built
            #     base.build_jet(heading=360 * np.random.random())


        mean = [(base.x, base.y) for base in myinfo["bases"]]
        mean = np.mean(mean, axis=0)

        min_dist = math.inf
        target = None
        if len(info) > 1:
            for name in info:
                if name != self.team:
                    if "bases" in info[name]:
                        for base in info[name]['bases']:
                            if np.linalg.norm(mean - (base.x, base.y)) < min_dist:
                                min_dist = np.linalg.norm(mean - (base.x, base.y))
                                target = (base.x, base.y)


        # # Try to find an enemy target
        # target = None
        # # If there are multiple teams in the info, find the first team that is not mine
        # if len(info) > 1:
        #     for name in info:
        #         if name != self.team:
        #             # Target only bases
        #             if "bases" in info[name]:
        #                 # Simply target the first base
        #                 t = info[name]["bases"][0]
        #                 target = [t.x, t.y]

        # Controlling my vehicles ==============================================

        # Description of information available on vehicles
        # (same info for tanks, ships, and jets):
        #
        # This is read-only information that all the vehicles (enemy and your own) have.
        # We define tank = info[team_name_1]["tanks"][0]. Then:
        #
        # tank.x (float): the x position of the tank
        # tank.y (float): the y position of the tank
        # tank.team (str): the name of the team the tank belongs to, e.g. ‘John’
        # tank.number (int): the player number
        # tank.speed (int): vehicle speed
        # tank.health (int): current health
        # tank.attack (int): vehicle attack force (how much damage it deals to enemy
        #     vehicles and bases)
        # tank.stopped (bool): True if the vehicle has been told to stop
        # tank.heading (float): the heading angle (in degrees) of the direction in
        #     which the vehicle will advance (0 = east, 90 = north, 180 = west,
        #     270 = south)
        # tank.vector (np.ndarray): the heading of the vehicle as a vector
        #     (basically equal to (cos(heading), sin(heading))
        # tank.position (np.ndarray): the (x, y) position as a numpy array
        # tank.uid (str): unique id for the tank
        #
        # Description of vehicle methods:
        #
        # If the vehicle is your own, the object will also have the following methods:
        #
        # tank.get_position(): returns current np.array([x, y])
        # tank.get_heading(): returns current heading in degrees
        # tank.set_heading(angle): set the heading angle (in degrees)
        # tank.get_vector(): returns np.array([cos(heading), sin(heading)])
        # tank.set_vector(np.array([vx, vy])): set the heading vector
        # tank.goto(x, y): go towards the (x, y) position
        # tank.stop(): halts the vehicle
        # tank.start(): starts the vehicle if it has stopped
        # tank.get_distance(x, y): get the distance between the current vehicle
        #     position and the given point (x, y) on the map
        # ship.convert_to_base(): convert the ship to a new base (only for ships).
        #     This only succeeds if there is land close to the ship.
        #
        # Note that by default, the goto() and get_distance() methods will use the
        # shortest path on the map (i.e. they may go through the map boundaries).

        # Iterate through all my tanks
        # if "tanks" in myinfo:
        #     for tank in myinfo["tanks"]:
        #         if (tank.uid in self.previous_positions) and (not tank.stopped):
        #             # If the tank position is the same as the previous position,
        #             # set a random heading
        #             if all(tank.position == self.previous_positions[tank.uid]):
        #                 tank.set_heading(np.random.random() * 360.0)
        #             # Else, if there is a target, go to the target
        #             elif target is not None:
        #                 tank.goto(*target)
        #         # Store the previous position of this tank for the next time step
        #         self.previous_positions[tank.uid] = tank.position

        if "tanks" in myinfo:
            for i, tank in enumerate(myinfo["tanks"]):
                # tank.stop()

                if i < 2:
                    tank.goto(tank.owner.x, tank.owner.y)

                if (tank.uid in self.previous_positions) and (not tank.stopped):
                    # If the tank position is the same as the previous position,
                    # set a random heading
                    if all(tank.position == self.previous_positions[tank.uid]):
                        tank.set_heading(np.random.random() * 360.0)
                        # tank.stop()

                    # Else, if there is a target, go to the target
                    # else:
                    #     h = np.random.random() * 2 * np.pi
                    #     x = 2*np.sin(h)
                    #     y = 2*np.cos(h)
                    #     tank.goto(tank.x + x, tank.y+y)
                    elif target:
                        tank.goto(*target)
                # # Store the previous position of this tank for the next time step
                self.previous_positions[tank.uid] = tank.position


        # Iterate through all my ships
        if "ships" in myinfo:
            for ship in myinfo["ships"]:
                if ship.uid in self.previous_positions:
                    # If the ship position is the same as the previous position,
                    # convert the ship to a base if it is far from the owning base,
                    # set a random heading otherwise
                    
                    if all(ship.position == self.previous_positions[ship.uid]):
                        if ship.get_distance(ship.owner.x, ship.owner.y) > 30:
                            ship.convert_to_base()
                        else:
                            ship.set_heading(np.random.random() * 360.0)
                    # else:
                    #     goal = find_closest_land(ship, game_map)
                    #     if goal:
                    #         ship.goto(*goal)
                # Store the previous position of this ship for the next time step
                self.previous_positions[ship.uid] = ship.position

        total = sum(list(self.njets.values()))

        # Iterate through all my jets
        if "jets" in myinfo:
            for jet in myinfo["jets"]:
                # Jets simply go to the target if there is one, they never get stuck
                if target is not None and total > 3:
                    jet.goto(*target)
                # else:
                    # jet.goto(*mean)



def find_closest_land(ship, map):
    x = ship.x
    y = ship.y
    # map = map[x-100:x+100, y-100:y+100]
    min_dist = math.inf
    min_xy = None
    
    for i in range(int(y)-50, int(y)+50):
        for j in range(int(x)-50, int(x)+50):
            d = np.linalg.norm((ship.x - j, ship.y - i))
            db = np.linalg.norm((ship.owner.x - j, ship.owner.y - i))
            if map[i, j] == 1 and d < min_dist and db > 20:
                min_dist = d
                min_xy = (j, i)
    return min_xy


# def is_goal(ship, x, y, game_map, info):
#     if game_map[y, x] != 1:
#         return False
