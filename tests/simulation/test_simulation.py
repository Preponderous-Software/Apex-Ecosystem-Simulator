from unittest.mock import MagicMock, call, patch

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

@patch("src.simulation.simulation.Water")
@patch("src.simulation.simulation.Rock")
@patch("src.simulation.simulation.Grass")
@patch("src.simulation.simulation.Berries")
@patch("src.simulation.simulation.BerryBush")
@patch("src.simulation.simulation.Chicken")
@patch("src.simulation.simulation.Pig")
@patch("src.simulation.simulation.Wolf")
@patch("src.simulation.simulation.Cow")
@patch("src.simulation.simulation.Fox")
@patch("src.simulation.simulation.Rabbit")
def test_generateMap(mock_rabbit, mock_fox, mock_cow, mock_wolf, mock_pig, mock_chicken, mock_berryBush, mock_berries, mock_grass, mock_rock, mock_water):
    # prepare
    testSim = getTestSimulation()
    testSim.config = MagicMock()
    testSim.config.numWaterEntities = 1
    testSim.config.numRockEntities = 1
    testSim.config.numGrassEntities = 1
    testSim.config.numBerriesEntities = 1
    testSim.config.numBerryBushEntities = 1
    testSim.config.numChickensToStart = 1
    testSim.config.numPigsToStart = 1
    testSim.config.numWolvesToStart = 1
    testSim.config.numCowsToStart = 1
    testSim.config.numFoxesToStart = 1
    testSim.config.numRabbitsToStart = 1
    testSim.addEntity = MagicMock()
    
    # execute
    testSim.generateMap()
    
    # assert
    mock_water.assert_called_once()
    mock_rock.assert_called_once()
    mock_grass.assert_called_once()
    mock_berries.assert_called_once()
    mock_berryBush.assert_called_once()
    mock_chicken.assert_called_once_with("Chicken")
    mock_pig.assert_called_once_with("Pig")
    mock_wolf.assert_called_once_with("Wolf")
    mock_cow.assert_called_once_with("Cow")
    mock_fox.assert_called_once_with("Fox")
    mock_rabbit.assert_called_once_with("Rabbit")
    
def test_placeEntities():
    # prepare
    testSim = getTestSimulation()
    grass1 = Grass()
    grass2 = Grass()
    testSim.entities = {1: grass1, 2: grass2}
    testSim.environment = MagicMock()
    testSim.environment.addEntity = MagicMock()
    
    # execute
    testSim.placeEntities()
    
    # assert
    testSim.environment.addEntity.assert_has_calls(
        [call(grass1), call(grass2)]
    )

def test_getNumberOfEntitiesOfType():
    # prepare
    testSim = getTestSimulation()
    grass1 = Grass()
    grass2 = Grass()
    testSim.entities = {1: grass1, 2: grass2}
    
    # execute
    result = testSim.getNumberOfEntitiesOfType(Grass)
    
    # assert
    assert result == 2

def test_getNumberOfLivingEntitiesOfType():
    # prepare
    testSim = getTestSimulation()
    chicken1 = Chicken("test chicken")
    chicken2 = Chicken("test chicken")
    testSim.entities = {1: chicken1, 2: chicken2}
    testSim.livingEntityIds = [1, 2]
    
    # execute
    result = testSim.getNumberOfLivingEntitiesOfType(Chicken)
    
    # assert
    assert result == 2
    
def test_getNumLivingEntities():
    # prepare
    testSim = getTestSimulation()
    chicken1 = Chicken("test chicken")
    chicken2 = Chicken("test chicken")
    testSim.entities = {1: chicken1, 2: chicken2}
    testSim.livingEntityIds = [1, 2]
    
    # execute
    result = testSim.getNumLivingEntities()
    
    # assert
    assert result == 2

def test_getNumExcrement():
    # prepare
    testSim = getTestSimulation()
    excrement1 = Excrement(1)
    excrement2 = Excrement(2)
    testSim.entities = {1: excrement1, 2: excrement2}
    testSim.excrementIds = [1, 2]
    
    # execute
    result = testSim.getNumExcrement()
    
    # assert
    assert result == 2

@patch("src.simulation.simulation.print")
def test_cleanup(print):
    # prepare
    testSim = getTestSimulation()
    testSim.environment = MagicMock()
    testSim.environment.printInfo = MagicMock()
    testSim.numTicks = 10
    
    # execute
    testSim.cleanup()
    
    # assert
    print.assert_has_calls(
        [call("---"), call("State of environment:"), call("Length of simulation:", 10, "ticks"), call("---")]
    )
    testSim.environment.printInfo.assert_called_once()

def test_update():
    # prepare
    testSim = getTestSimulation()
    testSim.initiateEntityActions = MagicMock()
    testSim.decreaseEnergyForLivingEntities = MagicMock()
    testSim.growGrass = MagicMock()
    testSim.growBerries = MagicMock()
    
    # execute
    testSim.update()
    
    # assert
    testSim.initiateEntityActions.assert_called_once()
    testSim.decreaseEnergyForLivingEntities.assert_called_once()
    testSim.growGrass.assert_called_once()
    testSim.growBerries.assert_called_once()

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

def test_performExcrementCheck_NoAction():
    # prepare
    testSim = getTestSimulation()
    excrement = Excrement(1)
    testSim.shouldExcrementTurnIntoGrass = MagicMock()
    testSim.shouldExcrementTurnIntoGrass.return_value = False
    testSim.removeEntity = MagicMock()
    testSim.addEntity = MagicMock()
    
    # execute
    testSim.performExcrementCheck(excrement)
    
    # assert
    testSim.shouldExcrementTurnIntoGrass.assert_called_once_with(excrement)
    testSim.removeEntity.assert_not_called()
    testSim.addEntity.assert_not_called()

def test_performExcrementCheck_StateChange():
    # prepare
    testSim = getTestSimulation()
    excrement = Excrement(1)
    excrement.getLocationID = MagicMock()
    excrement.getLocationID.return_value = 1
    testSim.shouldExcrementTurnIntoGrass = MagicMock
    testSim.shouldExcrementTurnIntoGrass.return_value = True
    testSim.removeEntity = MagicMock()
    testSim.addEntity = MagicMock()
    testSim.environment.getGrid().getLocation = MagicMock()
    testSim.environment.getGrid().getLocation.return_value = MagicMock()
    
    # execute
    testSim.performExcrementCheck(excrement)
    
    # assert
    testSim.addEntity.assert_called_once()

def test_growGrass():
    # prepare
    testSim = getTestSimulation()
    excrement = Excrement(1)
    testSim.excrementIds = [excrement.getID()]
    testSim.entities[excrement.getID()] = excrement
    testSim.performExcrementCheck = MagicMock()
    
    # execute
    testSim.growGrass()
    
    # assert
    testSim.performExcrementCheck.assert_called_once_with(excrement)

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

def test_growBerries_ShouldGainEnergy():
    # prepare
    testSim = getTestSimulation()
    berryBush = MagicMock()
    testSim.berryBushIds = [1]
    testSim.entities[1] = berryBush
    testSim.shouldBerryBushGainEnergy = MagicMock()
    testSim.shouldBerryBushGainEnergy.return_value = True
    testSim.performBerryBushCheck = MagicMock()
    
    # execute
    testSim.growBerries()
    
    # assert
    berryBush.incrementTick.assert_called_once()
    testSim.performBerryBushCheck.assert_called_once()

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
    testSim.environment.getGrid().getLocation.return_value = MagicMock()
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
    
    # execute
    result = testSim.countBerriesInLocation(location)
    
    # assert
    assert result == 1

def test_initiateEntityActions_NeedsEnergy():
    # prepare
    testSim = getTestSimulation()
    chicken = Chicken("test chicken")
    testSim.entities[chicken.getID()] = chicken
    testSim.livingEntityIds = [chicken.getID()]
    testSim.moveActionHandler = MagicMock()
    testSim.eatActionHandler = MagicMock()
    testSim.moveActionHandler.initiateMoveAction = MagicMock()
    testSim.eatActionHandler.initiateEatAction = MagicMock()
    chicken.needsEnergy = MagicMock()
    chicken.needsEnergy.return_value = True
    
    # execute
    testSim.initiateEntityActions()
    
    # assert
    testSim.moveActionHandler.initiateMoveAction.assert_called_once_with(chicken)
    testSim.eatActionHandler.initiateEatAction.assert_called_once_with(chicken, testSim.removeEntity)

def test_initiateEntityActions_EnergyNeedsMet_NoAction():
    # prepare
    testSim = getTestSimulation()
    chicken = Chicken("test chicken")
    testSim.entities[chicken.getID()] = chicken
    testSim.livingEntityIds = [chicken.getID()]
    testSim.moveActionHandler = MagicMock()
    testSim.eatActionHandler = MagicMock()
    testSim.excreteActionHandler = MagicMock()
    testSim.reproduceActionHandler = MagicMock()
    testSim.moveActionHandler.initiateMoveAction = MagicMock()
    testSim.eatActionHandler.initiateEatAction = MagicMock()
    testSim.excreteActionHandler.initiateExcreteAction = MagicMock()
    testSim.reproduceActionHandler.initiateReproduceAction = MagicMock()
    chicken.needsEnergy = MagicMock()
    chicken.needsEnergy.return_value = False
    testSim.shouldEntityExcrete = MagicMock()
    testSim.shouldEntityExcrete.return_value = False
    testSim.shouldEntityReproduce = MagicMock()
    testSim.shouldEntityReproduce.return_value = False
    
    # execute
    testSim.initiateEntityActions()
    
    # assert
    testSim.moveActionHandler.initiateMoveAction.assert_called_once_with(chicken)
    testSim.eatActionHandler.initiateEatAction.assert_not_called()
    testSim.excreteActionHandler.initiateExcreteAction.assert_not_called()
    testSim.reproduceActionHandler.initiateReproduceAction.assert_not_called()

def test_initiateEntityActions_EnergyNeedsMet_Excrete():
    # prepare
    testSim = getTestSimulation()
    chicken = Chicken("test chicken")
    testSim.entities[chicken.getID()] = chicken
    testSim.livingEntityIds = [chicken.getID()]
    testSim.moveActionHandler = MagicMock()
    testSim.eatActionHandler = MagicMock()
    testSim.excreteActionHandler = MagicMock()
    testSim.reproduceActionHandler = MagicMock()
    testSim.moveActionHandler.initiateMoveAction = MagicMock()
    testSim.eatActionHandler.initiateEatAction = MagicMock()
    testSim.excreteActionHandler.initiateExcreteAction = MagicMock()
    testSim.reproduceActionHandler.initiateReproduceAction = MagicMock()
    chicken.needsEnergy = MagicMock()
    chicken.needsEnergy.return_value = False
    testSim.shouldEntityExcrete = MagicMock()
    testSim.shouldEntityExcrete.return_value = True
    testSim.shouldEntityReproduce = MagicMock()
    testSim.shouldEntityReproduce.return_value = False
    
    # execute
    testSim.initiateEntityActions()
    
    # assert
    testSim.moveActionHandler.initiateMoveAction.assert_called_once_with(chicken)
    testSim.eatActionHandler.initiateEatAction.assert_not_called()
    testSim.excreteActionHandler.initiateExcreteAction.assert_called_once_with(chicken, testSim.addEntity, testSim.numTicks)
    testSim.reproduceActionHandler.initiateReproduceAction.assert_not_called()
    
def test_initiateEntityActions_EnergyNeedsMet_Reproduce():
    # prepare
    testSim = getTestSimulation()
    chicken = Chicken("test chicken")
    testSim.entities[chicken.getID()] = chicken
    testSim.livingEntityIds = [chicken.getID()]
    testSim.moveActionHandler = MagicMock()
    testSim.eatActionHandler = MagicMock()
    testSim.excreteActionHandler = MagicMock()
    testSim.reproduceActionHandler = MagicMock()
    testSim.moveActionHandler.initiateMoveAction = MagicMock()
    testSim.eatActionHandler.initiateEatAction = MagicMock()
    testSim.excreteActionHandler.initiateExcreteAction = MagicMock()
    testSim.reproduceActionHandler.initiateReproduceAction = MagicMock()
    chicken.needsEnergy = MagicMock()
    chicken.needsEnergy.return_value = False
    testSim.shouldEntityExcrete = MagicMock()
    testSim.shouldEntityExcrete.return_value = False
    testSim.shouldEntityReproduce = MagicMock()
    testSim.shouldEntityReproduce.return_value = True
    
    # execute
    testSim.initiateEntityActions()
    
    # assert
    testSim.moveActionHandler.initiateMoveAction.assert_called_once_with(chicken)
    testSim.eatActionHandler.initiateEatAction.assert_not_called()
    testSim.excreteActionHandler.initiateExcreteAction.assert_not_called()
    testSim.reproduceActionHandler.initiateReproduceAction.assert_called_once_with(chicken, testSim.addEntity)

def test_initiateEntityActions_EnergyNeedsMet_ExcreteAndReproduce():
    # prepare
    testSim = getTestSimulation()
    chicken = Chicken("test chicken")
    testSim.entities[chicken.getID()] = chicken
    testSim.livingEntityIds = [chicken.getID()]
    testSim.moveActionHandler = MagicMock()
    testSim.eatActionHandler = MagicMock()
    testSim.excreteActionHandler = MagicMock()
    testSim.reproduceActionHandler = MagicMock()
    testSim.moveActionHandler.initiateMoveAction = MagicMock()
    testSim.eatActionHandler.initiateEatAction = MagicMock()
    testSim.excreteActionHandler.initiateExcreteAction = MagicMock()
    testSim.reproduceActionHandler.initiateReproduceAction = MagicMock()
    chicken.needsEnergy = MagicMock()
    chicken.needsEnergy.return_value = False
    testSim.shouldEntityExcrete = MagicMock()
    testSim.shouldEntityExcrete.return_value = True
    testSim.shouldEntityReproduce = MagicMock()
    testSim.shouldEntityReproduce.return_value = True
    
    # execute
    testSim.initiateEntityActions()
    
    # assert
    testSim.moveActionHandler.initiateMoveAction.assert_called_once_with(chicken)
    testSim.eatActionHandler.initiateEatAction.assert_not_called()
    testSim.excreteActionHandler.initiateExcreteAction.assert_called_once_with(chicken, testSim.addEntity, testSim.numTicks)
    testSim.reproduceActionHandler.initiateReproduceAction.assert_called_once_with(chicken, testSim.addEntity)

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

def test_shouldExcrementTurnIntoGrass_False():
    # prepare
    testSim = getTestSimulation()
    testSim.config.grassGrowTime = 2
    testSim.numTicks = 1
    excrement = Excrement(1)
    
    # execute
    result = testSim.shouldExcrementTurnIntoGrass(excrement)
    
    # assert
    assert result == False
    
def test_shouldExcrementTurnIntoGrass_True():
    # prepare
    testSim = getTestSimulation()
    testSim.config.grassGrowTime = 2
    testSim.numTicks = 10
    excrement = Excrement(7)
    
    # execute
    result = testSim.shouldExcrementTurnIntoGrass(excrement)
    
    # assert
    assert result == True

@patch("src.simulation.simulation.random")
def test_shouldBerryBushGainEnergy_True(mock_random):
    # prepare
    testSim = getTestSimulation()
    mock_random.randrange.return_value = 5
    
    # execute
    result = testSim.shouldBerryBushGainEnergy()
    
    # assert
    assert result == True
    
@patch("src.simulation.simulation.random")
def test_shouldBerryBushGainEnergy_False(mock_random):
    # prepare
    testSim = getTestSimulation()
    mock_random.randrange.return_value = 50
    
    # execute
    result = testSim.shouldBerryBushGainEnergy()
    
    # assert
    assert result == False

@patch("src.simulation.simulation.random")
def test_shouldEntityExcrete_True(mock_random):
    # prepare
    testSim = getTestSimulation()
    mock_random.randrange.return_value = 5
    testSim.config.chanceToExcrete = 0.10
    
    # execute
    result = testSim.shouldEntityExcrete()
    
    # assert
    assert result == True
    
@patch("src.simulation.simulation.random")
def test_shouldEntityExcrete_False(mock_random):
    # prepare
    testSim = getTestSimulation()
    mock_random.randrange.return_value = 50
    testSim.config.chanceToExcrete = 0.10
    
    # execute
    result = testSim.shouldEntityExcrete()
    
    # assert
    assert result == False

@patch("src.simulation.simulation.random")
def test_shouldEntityReproduce_True(mock_random):
    # prepare
    testSim = getTestSimulation()
    mock_random.randrange.return_value = 5
    testSim.config.chanceToReproduce = 0.10
    
    # execute
    result = testSim.shouldEntityReproduce()
    
    # assert
    assert result == True

@patch("src.simulation.simulation.random")
def test_shouldEntityReproduce_False(mock_random):
    # prepare
    testSim = getTestSimulation()
    mock_random.randrange.return_value = 50
    testSim.config.chanceToReproduce = 0.10
    
    # execute
    result = testSim.shouldEntityReproduce()
    
    # assert
    assert result == False