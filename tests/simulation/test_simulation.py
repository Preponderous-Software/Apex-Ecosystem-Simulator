from unittest.mock import MagicMock, patch

from entity.berries import Berries
from entity.berryBush import BerryBush
from entity.chicken import Chicken
from entity.excrement import Excrement
from lib.pyenvlib.location import Location
import service
from src.simulation import simulation

# mock pygame
service.soundService.pygame = MagicMock()

def getTestSimulation():
    name = "my simulation"
    config = MagicMock()
    gameDisplay = MagicMock()
    gameDisplay.get_size.return_value = (1080, 720)
    return simulation.Simulation(name, config, gameDisplay)

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