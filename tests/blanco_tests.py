import re
from proboscis.asserts import *
from proboscis import test

from blanco import Class, \
                   Division, \
                   Level, \
                   Ring, \
                   Test


@test
def class_definition():
    """Establish definition of Class object."""
    c = Class(6, Level.INTRO, Test(Level.INTRO, "C"), Division.JUNIOR, Ring.ONE)
    assert_equal(c.id, 6)
    assert_equal(c.test, Test(Level.INTRO, "C"))
    assert_equal(c.division, Division.JUNIOR)
    assert_equal(c.ring, Ring.ONE)


@test
def test_definition():
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
