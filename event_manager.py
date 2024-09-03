import json
from datetime import datetime, timedelta
from collections import defaultdict

class EventManager:
    def __init__(self):
        self.events = {}  
        self.load_events()

    def create_event(self, name, category, start_time, duration):
        key = start_time.strftime('%Y-%m-%d %H:%M')
        duration = int(duration)
        if duration <= 0:
            print("Error: Duration must be a positive integer.")
            return
        # Check for conflicts
        conflicts = self.check_conflicts(start_time, duration)
        if conflicts:
            print("Conflict detected with the following events:")
            for conflict in conflicts:
                print(f"Time: {conflict[2]}, Name: {conflict[0]}, Category: {conflict[1]}, Duration: {conflict[3]} minutes")
            print("Please adjust the start time or duration to avoid conflicts.")
            return

        # Add the event if no conflicts, using a tuple to store event details
        self.events[key] = (name, category, start_time, duration)
        self.save_events()
        print("Event added successfully.")
        

    def keysgenerator(self, start_times):
        """Generator to yield events that match a specified list of start times."""
        for start_time in start_times:
            if isinstance(start_time, str):
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
                
            key = start_time.strftime('%Y-%m-%d %H:%M')
            if key in self.events:
                yield key, self.events[key]
            else:
                yield key, None  # Yield None if the event is not found

    def update_event(self, start_times, name=None, category=None, new_start=None, duration=None,sign=None):
        if isinstance(start_times, str):
            start_times = [start_times]

        event_gen = self.keysgenerator(start_times)  # Use the generator to iterate over keys

        for key, current_event in event_gen:
            if current_event is None:
                print(f"Event starting at {key} not found.")
                continue

                #sign 0 -> + , sign 1 -> -
            # Calculate new duration based on increment, decrement, or direct update
            if sign == 0 and duration is not None:
                new_duration = current_event[3] + duration
            elif sign == 1 and duration is not None:
                new_duration = max(5, current_event[3] - duration)  # Ensure duration does not go negative
            else:
                new_duration = duration if duration is not None else current_event[3]



            if new_start or duration is not None:
                conflicts = self.check_conflicts(new_start if new_start else datetime.strptime(key, '%Y-%m-%d %H:%M'), new_duration, key)
                if conflicts:
                    print("Conflict detected with the following events:")
                    for conflict in conflicts:
                        print(f"Time: {conflict[2]}, Name: {conflict[0]}, Category: {conflict[1]}, Duration: {conflict[3]} minutes")
                    print("Please adjust the start time or duration to avoid conflicts.")
                    return

            if new_start:
                # Skipping modification if `-new_start` is specified for multiple updates
                print(f"Skipping event update at {key} because `-new_start` is not allowed for multiple updates.")
                continue

            # Update event details
            self.events[key] = (
                name if name else current_event[0],
                category if category else current_event[1],
                current_event[2],
                new_duration
            )

            self.save_events()
            print(f"Event starting at {key} updated successfully.")


    def delete_event(self, key):
        if key in self.events:
            del self.events[key]
            self.save_events()
            print("Event deleted successfully.")
        else:
            print("Event not found.")

    def list_events(self):
        return self.events

    def check_conflicts(self, new_start_time, new_duration, ignore_key=None):
        conflicts = []
        new_end_time = new_start_time + timedelta(minutes=new_duration)
        for key, event in self.events.items():
            event_start_time = datetime.strptime(key, '%Y-%m-%d %H:%M')
            event_end_time = event_start_time + timedelta(minutes=event[3])

            if key != ignore_key and not (new_start_time >= event_end_time or new_end_time <= event_start_time):
                conflicts.append(event)
        return conflicts

    def save_events(self):
        with open('events.json', 'w') as file:
            # Convert tuple events to a list before saving, since JSON does not support tuples directly
            json.dump({k: list(v) for k, v in self.events.items()}, file, default=str)

    def load_events(self):
        try:
            with open('events.json', 'r') as file:
                # Load events and convert lists back to tuples
                self.events = {k: tuple(v) for k, v in json.load(file).items()}
        except FileNotFoundError:
            self.events = {}
        except json.JSONDecodeError:
            self.events = {}

    def filter_events_by_category(self, category):
        """Generator to yield events that match a specified category."""
        for key, event in self.events.items():
            if event[1].lower() == category.lower():
                yield key, event

    def event_generator(self):
        """Generator to yield events one by one."""
        for key, event in self.events.items():
            yield key, event


    def generate_report(self):
        """Generates reports on total time spent per category, busiest days, and trends over time."""
        total_time_per_category = defaultdict(int)
        events_per_day = defaultdict(int)
        trends_per_day = defaultdict(lambda: defaultdict(int))  # {date: {category: total_duration}}

        event_gen = self.event_generator()

        for key, event in event_gen:
            name, category, start_time, duration = event
            date = datetime.strptime(key, '%Y-%m-%d %H:%M').date()
            
            total_time_per_category[category] += duration
            events_per_day[date] += 1
            trends_per_day[date][category] += duration

        # Preparing the report content
        report_content = []
        
        # Total time spent per category
        report_content.append("Total Time Spent per Category:")
        for category, total_time in total_time_per_category.items():
            report_content.append(f"Category: {category}, Total Time: {total_time} minutes")

        # Busiest days (most events)
        busiest_days = sorted(events_per_day.items(), key=lambda x: x[1], reverse=True)
        report_content.append("\nBusiest Days:")
        for day, count in busiest_days:
            report_content.append(f"Date: {day}, Number of Events: {count}")

        # Trends over time by category
        report_content.append("\nTrends Over Time by Category:")
        for day, categories in sorted(trends_per_day.items()):
            report_content.append(f"Date: {day}")
            for category, total_duration in sorted(categories.items()):
                report_content.append(f"  Category: {category}, Total Time: {total_duration} minutes")

        # Write report to a file
        current_time = datetime.now().strftime('%Y_%m_%d')
        report_filename = f"report_{current_time}.log"
        with open(report_filename, 'w') as file:
            file.write("\n".join(report_content))

        # Print the report content to the terminal
        for line in report_content:
            print(line)
        print(f"Report generated and saved as {report_filename}.")
