import pytest
from unittest.mock import patch, mock_open
from datetime import datetime
from event_manager import EventManager

@pytest.fixture
def events():
    # Mock the open function in the context of EventManager
    with patch('builtins.open', mock_open(read_data="{}")) as mock_file:
        # Initialize an EventScheduler instance using the mock
        events = EventManager()
        events.create_event("Meeting", "Work", datetime.strptime("2024-09-04 12:00", "%Y-%m-%d %H:%M"), 30)
        events.create_event("Break", "Personal", datetime.strptime("2024-09-04 15:00", "%Y-%m-%d %H:%M"), 45)
        events.create_event("Date", "Personal", datetime.strptime("2024-09-05 18:00", "%Y-%m-%d %H:%M"), 80)
        yield events

def test_list_events(events):
    """Test listing all events"""
    listed_events = events.list_events()
    expected_events = {
        "2024-09-04 12:00": ("Meeting", "Work", datetime.strptime("2024-09-04 12:00", "%Y-%m-%d %H:%M"), 30),
        "2024-09-04 15:00": ("Break", "Personal", datetime.strptime("2024-09-04 15:00", "%Y-%m-%d %H:%M"), 45),
        "2024-09-05 18:00": ("Date", "Personal", datetime.strptime("2024-09-05 18:00", "%Y-%m-%d %H:%M"), 80)
    }
    assert len(listed_events) == len(expected_events)
    for key, value in expected_events.items():
        assert key in listed_events
        assert listed_events[key] == value


def test_add_event(events):
    """Test adding a new event"""
    events.create_event("Reading", "Leisure", datetime.strptime("2024-09-11 19:00", "%Y-%m-%d %H:%M"), 60)
    assert "2024-09-11 19:00" in events.events
    assert events.events["2024-09-11 19:00"][0] == "Reading"


def test_delete_event(events):
    """Test deleting an existing event"""
    events.delete_event("2024-09-04 12:00")
    assert "2024-09-04 12:00" not in events.events

def test_update_event(events):
    """Test updating an existing event"""
    events.update_event(["2024-09-04 12:00"], name="Important Meeting")
    assert events.events["2024-09-04 12:00"][0] == "Important Meeting"


def test_conflict_detection(events):
    """Test conflict detection when adding overlapping events"""
    with pytest.raises(ValueError, match="Conflict detected"):
        events.create_event("GYM", "Exercises", datetime.strptime("2024-09-04 15:30", "%Y-%m-%d %H:%M"), 30)


def test_filter_by_category(events):
    """Test filtering events by category"""
    filtered_events = list(events.filter_events_by_category("Work"))
    assert len(filtered_events) == 1
    assert filtered_events[0][1][0] == "Meeting"