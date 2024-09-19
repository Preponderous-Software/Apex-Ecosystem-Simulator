from unittest.mock import MagicMock, patch

from entity.berries import Berries
from entity.berryBush import BerryBush
from entity.chicken import Chicken
from entity.excrement import Excrement
from entity.grass import Grass
from lib.pyenvlib.location import Location
import service
from src.simulation import simulation

# mock pygame
service.soundService.pygame = MagicMock()

# helper methods -------------------------------------------------------------
def getTestSimulation():
    name = "my simulation"
    config = MagicMock()
    gameDisplay = MagicMock()
    gameDisplay.get_size.return_value = (1080, 720)
    return simulation.Simulation(name, config, gameDisplay)

# constructor tests ----------------------------------------------------------
def test_initialization():
    # prepare
    name = "my simulation"
    config = MagicMock()
    gameDisplay = MagicMock()
    gameDisplay.get_size.return_value = (1080, 720)
    
    # execute
    testSim = simulation.Simulation(name, config, gameDisplay)
    
    # assert
    assert testSim.name == name
    assert testSim.config == config
    assert testSim.gameDisplay == gameDisplay
    assert testSim.environment is not None

# public method tests --------------------------------------------------------
def test_initializeLocationWidthAndHeight():
    # prepare
    testSim = getTestSimulation()
    testSim.environment = MagicMock()
    testSim.environment.getGrid().getRows.return_value = 10
    testSim.environment.getGrid().getColumns.return_value = 10
     
    # execute
    testSim.initializeLocationWidthAndHeight()
    
    # assert
    assert testSim.locationWidth == 108
    assert testSim.locationHeight == 72

def test_addEntity_Grass():
    # prepare
    testSim = getTestSimulation()
    grass = MagicMock()
    grass.getID.return_value = 1
    
    # execute
    testSim.addEntity(grass)
    
    # assert
    assert testSim.entities[1] == grass
    assert 1 not in testSim.livingEntityIds
    assert 1 not in testSim.excrementIds
    assert 1 not in testSim.berryBushIds

def test_addEntity_Chicken():
    # prepare
    testSim = getTestSimulation()
    chicken = Chicken("test chicken")
    
    # execute
    testSim.addEntity(chicken)
    
    # assert
    assert testSim.entities[chicken.getID()] == chicken
    assert chicken.getID() in testSim.livingEntityIds
    assert chicken.getID() not in testSim.excrementIds
    assert chicken.getID() not in testSim.berryBushIds

def test_addEntity_Excrement():
    # prepare
    testSim = getTestSimulation()
    tick = 1
    excrement = Excrement(tick)
    
    # execute
    testSim.addEntity(excrement)
    
    # assert
    assert testSim.entities[excrement.getID()] == excrement
    assert excrement.getID() not in testSim.livingEntityIds
    assert excrement.getID() in testSim.excrementIds
    assert excrement.getID() not in testSim.berryBushIds

def test_addEntity_BerryBush():
    # prepare
    testSim = getTestSimulation()
    berryBush = BerryBush()
    
    # execute
    testSim.addEntity(berryBush)
    
    # assert
    assert testSim.entities[berryBush.getID()] == berryBush
    assert berryBush.getID() not in testSim.livingEntityIds
    assert berryBush.getID() not in testSim.excrementIds
    assert berryBush.getID() in testSim.berryBushIds

# def test_generateMap():
#     assert False
    
# def test_placeEntities():
#     assert False

# def test_getNumberOfEntitiesOfType():
#     assert False

# def test_getNumberOfLivingEntitiesOfType():
#     assert False
    
# def test_getNumLivingEntities():
#     assert False

# def test_getNumExcrement():
#     assert False

# def test_cleanup():
#     assert False

# def test_update():
#     assert False

# private method tests -------------------------------------------------------
def test_removeEntityFromLocation():
    # prepare
    testSim = getTestSimulation()
    entity = MagicMock()
    testSim.environment.getGrid().getLocation = MagicMock()
    testSim.environment.getGrid().getLocation.return_value = MagicMock()
    
    # execute
    testSim.removeEntityFromLocation(entity)
    
    # assert
    testSim.environment.getGrid().getLocation.assert_called_once()
    testSim.environment.getGrid().getLocation().removeEntity.assert_called_once()

@patch("src.simulation.simulation.print")
def test_printDeathInfo_notOldest(print):
    # prepare
    testSim = getTestSimulation()
    entity = MagicMock()
    entity.getName.return_value = "test entity"
    oldestLivingEntity = MagicMock()
    testSim.livingEntityIds = [1]
    testSim.entities[1] = oldestLivingEntity
    
    # execute
    testSim.printDeathInfo(entity, oldestLivingEntity)
    
    # assert
    print.assert_called_once_with("test entity has died.")

@patch("src.simulation.simulation.print")
def test_printDeathInfo_isOldest(print):
    # prepare
    testSim = getTestSimulation()
    entity = MagicMock()
    entity.getName.return_value = "test entity"
    entity.getID.return_value = 1
    oldestLivingEntity = MagicMock()
    oldestLivingEntity.getID.return_value = 1
    testSim.livingEntityIds = [1]
    testSim.entities[1] = oldestLivingEntity
    
    # execute
    testSim.printDeathInfo(entity, oldestLivingEntity)
    
    # assert
    print.assert_called_once_with("test entity has died. They were the oldest living entity.")

def test_removeEntity():
    # prepare
    testSim = getTestSimulation()
    entity = MagicMock()
    entity.getID.return_value = 1
    testSim.entities[1] = entity
    testSim.livingEntityIds = []
    testSim.excrementIds = []
    testSim.berryBushIds = []
    testSim.removeEntityFromLocation = MagicMock()
    
    # execute
    testSim.removeEntity(entity)
    
    # assert
    assert 1 not in testSim.entities
    testSim.removeEntityFromLocation.assert_called_once()

def test_removeEntity_Excrement():
    # prepare
    testSim = getTestSimulation()
    entity = Excrement(1)
    testSim.entities[entity.getID()] = entity
    testSim.livingEntityIds = []
    testSim.excrementIds = [entity.getID()]
    testSim.berryBushIds = []
    testSim.removeEntityFromLocation = MagicMock()
    
    # execute
    testSim.removeEntity(entity)
    
    # assert
    assert entity.getID() not in testSim.entities
    testSim.removeEntityFromLocation.assert_called_once()
    assert entity.getID() not in testSim.excrementIds

def test_removeEntity_BerryBush():
    # prepare
    testSim = getTestSimulation()
    entity = BerryBush()
    testSim.entities[entity.getID()] = entity
    testSim.livingEntityIds = []
    testSim.excrementIds = []
    testSim.berryBushIds = [entity.getID()]
    testSim.removeEntityFromLocation = MagicMock()
    
    # execute
    testSim.removeEntity(entity)
    
    # assert
    assert entity.getID() not in testSim.entities
    testSim.removeEntityFromLocation.assert_called_once()
    assert entity.getID() not in testSim.berryBushIds

def test_removeEntity_Chicken_NotMuted():
    # prepare
    testSim = getTestSimulation()
    entity = Chicken("test chicken")
    testSim.entities[entity.getID()] = entity
    testSim.livingEntityIds = [entity.getID()]
    testSim.excrementIds = []
    testSim.berryBushIds = []
    testSim.removeEntityFromLocation = MagicMock()
    testSim.soundService = MagicMock()
    testSim.config.muted = False
    
    # execute
    testSim.removeEntity(entity)
    
    # assert
    assert entity.getID() not in testSim.entities
    testSim.removeEntityFromLocation.assert_called_once()
    assert entity.getID() not in testSim.livingEntityIds
    testSim.soundService.playDeathSoundEffect.assert_called_once()

def test_removeEntity_Chicken_Muted():
    # prepare
    testSim = getTestSimulation()
    entity = Chicken("test chicken")
    testSim.entities[entity.getID()] = entity
    testSim.livingEntityIds = [entity.getID()]
    testSim.excrementIds = []
    testSim.berryBushIds = []
    testSim.removeEntityFromLocation = MagicMock()
    testSim.soundService = MagicMock()
    testSim.config.muted = True
    
    # execute
    testSim.removeEntity(entity)
    
    # assert
    assert entity.getID() not in testSim.entities
    testSim.removeEntityFromLocation.assert_called_once()
    assert entity.getID() not in testSim.livingEntityIds
    testSim.soundService.playDeathSoundEffect.assert_not_called()

# def test_performExcrementCheck():
#     assert False

# def test_growGrass():
#     assert False

def test_growBerries():
    # prepare
    testSim = getTestSimulation()
    berryBush = MagicMock()
    testSim.berryBushIds = [1]
    testSim.entities[1] = berryBush
    testSim.performBerryBushCheck = MagicMock()
    
    # execute
    testSim.growBerries()
    
    # assert
    berryBush.incrementTick.assert_called_once()
    testSim.performBerryBushCheck.assert_called_once()

def test_growBerries_noBerryBush():
    # prepare
    testSim = getTestSimulation()
    testSim.berryBushIds = []
    testSim.performBerryBushCheck = MagicMock()
    
    # execute
    testSim.growBerries()
    
    # assert
    assert testSim.performBerryBushCheck.call_count == 0

def test_performBerryBushCheck_notTime():
    # prepare
    testSim = getTestSimulation()
    berryBush = MagicMock()
    berryBush.getTick.return_value = 1
    testSim.config.berryBushGrowTime = 2
    testSim.environment.getGrid().getLocation = MagicMock()
    testSim.environment.getGrid().getLocation.return_value = MagicMock()
    
    # execute
    testSim.performBerryBushCheck(berryBush)
    
    # assert
    testSim.environment.getGrid().getLocation.assert_not_called()

def test_performBerryBushCheck_notEnoughEnergy():
    # prepare
    testSim = getTestSimulation()
    berryBush = MagicMock()
    berryBush.getTick.return_value = 2
    berryBush.getEnergy.return_value = 5
    testSim.config.berryBushGrowTime = 2
    testSim.environment.getGrid().getLocation = MagicMock()
    testSim.environment.getGrid().getLocation.return_value = MagicMock()
    
    # execute
    testSim.performBerryBushCheck(berryBush)
    
    # assert
    testSim.environment.getGrid().getLocation.assert_not_called()

def test_performBerryBushCheck_tooManyBerries():
    # prepare
    testSim = getTestSimulation()
    berryBush = MagicMock()
    berryBush.getTick.return_value = 2
    berryBush.getEnergy.return_value = 20
    testSim.config.berryBushGrowTime = 2
    testSim.environment.getGrid().getLocation = MagicMock()
    testSim.countBerriesInLocation = MagicMock()
    testSim.countBerriesInLocation.return_value = 10
    testSim.addEntity = MagicMock()
    
    # execute
    testSim.performBerryBushCheck(berryBush)
    
    # assert
    testSim.addEntity.assert_not_called()

def test_performBerryBushCheck_Success():
    # prepare
    testSim = getTestSimulation()
    berryBush = MagicMock()
    berryBush.getTick.return_value = 2
    berryBush.getEnergy.return_value = 20
    testSim.config.berryBushGrowTime = 2
    testSim.environment.getGrid().getLocation = MagicMock()
    testSim.countBerriesInLocation = MagicMock()
    testSim.countBerriesInLocation.return_value = 9
    testSim.addEntity = MagicMock()
    
    # execute
    testSim.performBerryBushCheck(berryBush)
    
    # assert
    testSim.addEntity.assert_called_once()

def test_countBerriesInLocation():
    # prepare
    testSim = getTestSimulation()
    location = Location(1, 1)
    berries = Berries()
    location.addEntity(berries)
    testSim.environment.getEntity = MagicMock()
    testSim.environment.getEntity.return_value = berries
    
    # execute
    result = testSim.countBerriesInLocation(location)
    
    # assert
    assert result == 1

# def test_initiateEntityActions():
#     assert False

def test_decreaseEnergyForLivingEntities():
    # prepare
    testSim = getTestSimulation()
    chicken = Chicken("test chicken")
    chicken.decreaseEnergy = MagicMock()
    testSim.entities[chicken.getID()] = chicken
    testSim.livingEntityIds = [chicken.getID()]
    chicken.removeEnergy = MagicMock()
    
    # execute
    testSim.decreaseEnergyForLivingEntities()
    
    # assert
    chicken.removeEnergy.assert_called_once_with(1)

def test_decreaseEnergyForLivingEntities_OutOfEnergy():
    # prepare
    testSim = getTestSimulation()
    chicken = Chicken("test chicken")
    chicken.decreaseEnergy = MagicMock()
    chicken.getEnergy = MagicMock()
    chicken.getEnergy.return_value = 0
    chicken.removeEnergy = MagicMock()
    testSim.entities[chicken.getID()] = chicken
    testSim.livingEntityIds = [chicken.getID()]
    testSim.removeEntity = MagicMock()
    
    # execute
    testSim.decreaseEnergyForLivingEntities()
    
    # assert
    chicken.removeEnergy.assert_called_once_with(1)
    testSim.removeEntity.assert_called_once_with(chicken)