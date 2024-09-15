from src.ui import textAlert

def test_initialization():
    # prepare
    x = 10
    y = 20
    size = 30
    color = (255, 255, 255)
    duration = 5
    
    # execute
    alert = textAlert.TextAlert(x, y, size, color, duration)
    
    # assert
    assert alert.x == x
    assert alert.y == y
    assert alert.text == []
    assert alert.size == size
    assert alert.color == color
    assert alert.duration == duration

def test_addLine():
    # prepare
    alert = textAlert.TextAlert(0, 0, 0, (0, 0, 0), 0)
    
    # execute
    alert.addLine("Hello, world!")
    
    # assert
    assert alert.text == ["Hello, world!"]