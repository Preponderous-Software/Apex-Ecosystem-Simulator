from unittest.mock import MagicMock, patch

from entity.berryBush import BerryBush
from src.simulation import simulation

def getTestSimulation():
    name = "my simulation"
    config = MagicMock()
    gameDisplay = MagicMock()
    gameDisplay.get_size.return_value = (1080, 720)
    return simulation.Simulation(name, config, gameDisplay)

@patch('service.soundService.pygame')
def test_initialization(mock_pygame):
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
    
@patch('service.soundService.pygame')
def test_growBerries(mock_pygame):
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

@patch('service.soundService.pygame')
def test_growBerries_noBerryBush(mock_pygame):
    # prepare
    testSim = getTestSimulation()
    testSim.berryBushIds = []
    testSim.performBerryBushCheck = MagicMock()
    
    # execute
    testSim.growBerries()
    
    # assert
    assert testSim.performBerryBushCheck.call_count == 0

@patch('service.soundService.pygame')
def test_performBerryBushCheck_notTime(mock_pygame):
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

@patch('service.soundService.pygame')
def test_performBerryBushCheck_notEnoughEnergy(mock_pygame):
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

@patch('service.soundService.pygame')
def test_performBerryBushCheck_tooManyBerries(mock_pygame):
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

@patch('service.soundService.pygame')
def test_performBerryBushCheck_Success(mock_pygame):
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

@patch('service.soundService.pygame')
def countBerriesInLocation(mock_pygame):
    # prepare
    testSim = getTestSimulation()
    location = MagicMock()
    location.getEntities.return_value = [BerryBush(), BerryBush()]
    
    # execute
    result = testSim.countBerriesInLocation(location)
    
    # assert
    assert result == 2