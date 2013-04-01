import re
from proboscis.asserts import *
from proboscis import test


class Award(object):
    """
    Level
      ** Division - later
    Like "Champion" or "Reserve".  Its just a level of reward.
    Lets assume they are mapped to the level.

    """
    def __init__(self, level):
      self.level = level


class Class(object):
    """
    A class is an instance of a test matched with a division. A class may have
    multiple riders in it, meaning there are multiple rides for each class.
    Also is assigned to a ring.
    """

    def __init__(self, id, level, test, division, ring):
        self.id = id
        self.level = level
        self.test = test
        self.division = division
        self.ring = ring
        self.maximum_points = 0 # USDF can change this for
        self.time = 0 # the time USDF says it should take

    @classmethod
    def legacy_load_all(cls, db):
        return [cls.legacy_from_row(row)
                for row in db.execute("SELECT * FROM Classes")]

    @classmethod
    def legacy_from_row(cls, row):
        id = row[0]
        if row[1] is not None:
            level = Level.find_or_create(row[1])
        else:
            level = None
        test = row[2]
        if row[3] is not None:
            division = Division.find_or_create(row[3])
        else:
            division = None
        ring = row[7]
        return cls(id, level, test, division, ring) 

    def __str__(self):
        return "%s %s %s %s" % (self.id, self.level, self.test, self.division)

    @test
    def definition():
        """Establish definition of Class object."""
        c = Class(6, Test(Level.INTRO, "C"), Division.JUNIOR, Ring.ONE)
        assert_equal(c.id, 6)
        assert_equal(c.test, Test(Level.INTRO, "C"))
        assert_equal(c.division, Division.JUNIOR)
        assert_equal(c.ring, Ring.ONE)


class ClassShow(object):
    """
    Maps a class to a show.
    Date -
    Available() - If any rides for this class, true, else false.
    Ring - The ring they're in for that show
    Points - Maximum number of points this test can have
    Interval - (timedelta) Length of time the test takes.
    Order - aka "Order of Go" Its just a number. This determines the schedule.
    Time - Sometimes this is needed to say "it must start at a certain time."
    Judge - At LHF a class only has one judge. Other places may have multiple judges for a class.
    description() - A string created by "{Level} {Test#} {Division}"
    """

    def __init__(self, ring_number, max_points, interval, order_of_go, time,
                 judges=None):
        self.ring_number = ring_number
        self.max_points = max_points
        self.interval = interval
        self.order_of_go = order_of_go
        self.time = time
        self.judges = judges or []

    @property
    def description(self):
        return "%s %s %s" % (level)


class Division(object):
    """
    Division
    Summary:
     These are the quality of the rider.
     For example, there is adult, an open rider, juniors, etc.
     An open rider cannot ride in adult, because they are not an amateur.
     A junior can't ride in adult, and adult can't ride in junior.
     They are aged based, except for adult and open rider.
     Open riders are professionals.
     What a rider is actually listed in is up to show management.
     The divisions however are always the same.
    """

    DIVISIONS = {}

    def __init__(self, name):
        if name is None:
            raise TypeError("Must be string, not None.")
        self.name = name

    def __eq__(self, rhs):
        return self.name == rhs.name

    @classmethod
    def find_or_create(cls, name):
        if name not in cls.DIVISIONS:
            cls.DIVISIONS[name] = Division(name)
        return cls.DIVISIONS[name]

    def __str__(self):
        return self.name


# Division._12_AND_UNDER = Division("12 and Under")
# Division._13_AND_OVER = Division("13 and Over")
# Division.ADULT = Division("Adult")
# Division.JUNIOR = Division("Junior")
# Division.OPEN_RIDER = Division("Open Rider")



class Entrant(object):
    """A rider who has entered a show."""

    def __init__(self, rider, division):
        self.rider = rider
        self.division = division

    def __eq__(self):
        return self.rider == rhs.rider and self.division == rhs.division

    def __str__(self):
        return "%s (%s)" % (rider, division)


class Entry(object):
    """
    The pairing of a horse and rider. It is uniquely identified per show by a
    bridal tag.

    There's a list of these.
    Bridal Tag Number - Key. How you find everything.
    Horse -
    RiderAndDivision -
    Rides - a list of rides
    At runtime, they want them to be able to change rides to different entries
    """

    def __init__(self, bridal_tag, entrant, horse):
        self.bridal_tag = bridal_tag
        self.entrant = entrant
        self.horse = horse

    def __eq__(self, rhs):
        return self.bridal_tag == rhs.bridal_tag

    def __str__(self):
        return "%s riding %s" % (entrant, horse)


class Horse(object):

    def __init__(self, name):
        self.name = name    

    @classmethod
    def legacy_load_all(cls, db):
        return [cls.legacy_from_row(row) 
                for row in db.execute("SELECT * FROM Horses;")]

    @classmethod
    def legacy_from_row(cls, row):
        return cls(row[0]) 

    def __str__(self):
        return self.name


class Level(object):

    STUFF = {}

    def __init__(self, name, id_pattern=None):
        if name is None:
            raise TypeError("NO!")
        self.name = name
        self.id_pattern = id_pattern

    def __eq__(self, other):
        return self.name == other.name

    @classmethod
    def find_or_create(cls, name):
        if name not in cls.STUFF:
            cls.STUFF[name] = Level(name)
        return cls.STUFF[name]

    # @classmethod
    # def legacy_load_all(cls, db):
    #     return [cls.legacy_from_row(row) 
    #             for row in db.execute("SELECT * FROM Horses;")]

    # @classmethod
    # def legacy_from_row(cls, row):
    #     return cls.find_or_create(row[1]) 

    def __str__(self):
        return self.name

# Level._1ST = Level("1st", "[0-9]+")
# Level._2ND = Level("2nd", "[0-9]+")
# Level._3RD = Level("3rd", "[0-9]+")
# Level._4RTH = Level("4rth", "[0-9]+")
# Level.INTRO = Level("Intro", "[A-Z]+")
# Level.PRIX_ST_GEORGES = Level("Prix St. Georges", "^$")  #empty
# Level.TRAINING = Level("Training", "[0-9]+")


class Id(object):
    """
    This appears in printed reports and is short hand for the class. Like
    "12A" is "First 2 Adult"
    """

    def __init__(self, value):
      self.value = value;

    def __str__(self):
      return self.value;


class Ride(object):
    """A class, plus an entry.

    One entry won't take the same class twice so this is unique per show.

    """

    def __init__(self, entry, cls):
        self.entry = entry
        self.cls = cls

    def __eq__(self, rhs):
        return self.entry == rhs.entry and self.cls == rhs.cls

    def __str__(self):
        return "%s, %s" % (self.entry, self.cls)


class Rider(object):
    """An entrant who rides upon a beast of burden."""

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __eq__(self, rhs):
        return self.first_name  == rhs.first_name \
               and self.last_name == rhs.last_name

    def __str__(self):
        return self.first_name + " " + last_name


class Ring(object):
    """Each class goes to one ring."""

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __eq__(self, rhs):
        return self.name == rhs.name

    def __str__(self):
        return self.name

Ring.ONE = Ring("One", "")
Ring.TWO = Ring("Two", "")


class Show(object):
    """
    An instance of the show
    Show Title - This gets printed out on the screen
    Start Date - The date of the show!
    """

    def __init__(self, title, date):
      self.title = title
      self.date = date


class Test(object):
    """Identifies a test.

    Level - The level of the test.
    Test Number - A number of some other ID (like letters) that identifies a test within a level.

    """

    def __init__(self, level, id):
        self.level = level
        id_as_str = str(id)
        matches = re.match(level.id_pattern, id_as_str)
        if not matches:
            raise ValueError("Test \"%s\" does not match the pattern for "
                             "level %s." % (test, level))
        self.id = id_as_str

    def __eq__(self, other):
        return self.level == other.level and self.id == other.id

    def __str__(self):
        return "%s %s" % (self.level, self.id)

    @test
    def definition():
        """Establish structure of TestID."""
        test = Test(Level.INTRO, "B")
        assert_equal(test.level, Level.INTRO)
        assert_equal(test.id, "B")
        assert_equal(test, Test(Level.INTRO, "B"))

        test = Test(Level.TRAINING, 1)
        assert_equal(test.level, Level.TRAINING)
        assert_equal(test.id, "1")
        assert_equal(test, Test(Level.TRAINING, 1))

    @test
    def test_must_match_level_format():
        """The level must match the level format."""
        Test(Level.INTRO, "B")
        assert_raises(ValueError, Test, Level.INTRO, "3")
        assert_raises(ValueError, Test, Level.INTRO, "b")
        assert_raises(ValueError, Test, Level.PRIX_ST_GEORGES, "C")

# ClassList - a list of classes



# Judge - A judge! Just a person



# Level Score Criteria
#   Level - Level of skill (see Level)
#   Required number of rides for that award - The minimum rides a rider must ride in that level to be
#     eligible for the award
#   AverageScore(rider) - given a rider, if that rider has riden the required number of rides, takes the top
#     {required number} or rides from their list of ride scores in that level and averages those together
#     score.  Doesn't penalize a person for a lot of rides, but if you don't do a lot of rides you better be good.
#   Says "Program, go into each level and pull out everyone who had {minimum number} rides and compute the average.
#   NOTE: In the future they want this to be by division but first lets test the old show data. The old
#   program didn't do this, so lets make sure we can

# Level Score
#   Rider
#   Score
#   Level
#   - See above, its either N/A if the rider did not take "required rides" for that level, or its the avg
#     of the top {required rides} they had in that level.



# Ride
#   A class,
#   plus an entry - they want that to be maybe different
#   plus whether or not its a scratch

# Rider
#   Identification info for a rider

# RiderAndDivision
#   Rider
#   Division - has their division for this show

# Ring
#   A ring a show is in.
#   ClassList

# Schedule


# ShowAward
#   Instant of the award handed out at each show to a rider conditions permitting
#   Division
#   Level
#   Take a list of all level scores.
#   Find all level scores with the given divison and score.
#   If the number of levelscores is less than 2, then that person didn't compete with anyone so they don't win
#   anything :(
#   But if now, then the highests levelscore's rider gets the award

# Test
