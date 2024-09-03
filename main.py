import argparse
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from event_scheduler.event_manager import EventManager # type: ignore

def main():
    parser = argparse.ArgumentParser(description="Event Scheduler and Analyzer CLI")

  
    # Add Event
    parser.add_argument('-add', action='store_true', help="Add a new event. Requires -name, -category, -start, -duration")
    parser.add_argument('-name', type=str, help="Name of the event.use with \" \" ")
    parser.add_argument('-category', type=str, help="Category of the event. use with \" \"")
    parser.add_argument('-start', type=str, help="Start time of the event (format: \"YYYY-MM-DD HH:MM\")")
    parser.add_argument('-duration', type=str, help="Duration of the event in minutes or an increment/decrement (e.g., +10)")
    # Update Event
    parser.add_argument('-update', action='store_true', help="Update an event or list of events using -keys. Requires one or more of [-start,-name,-category,-duration]")
    parser.add_argument('-keys', type=str, nargs='+', help='list of start times to update(Use \"YYYY-MM-DD HH:MM\" space-separated)')

    # Delete Event
    parser.add_argument('-delete', action='store_true', help="Delete an event. Requires -start")

    # List Events
    parser.add_argument('-list', action='store_true', help="List all events")

    # Filter Events
    parser.add_argument('-filter', action='store_true', help="Filter events by category. Requires -category")

    # Generate Report
    parser.add_argument('-report', action='store_true', help="Generate a report on events")

    args = parser.parse_args()

    manager = EventManager()


    if not any([args.add, args.delete, args.update, args.list, args.filter , args.report]):
        parser.print_help()
        return


    if args.add:
        if not (args.name and args.category and args.start and args.duration):
            print("Error: Missing required arguments for adding an event.")
            print("Usage: -add -name NAME -category CATEGORY -start 'YYYY-MM-DD HH:MM' -duration DURATION")
            return

        try:
            start_time = datetime.strptime(args.start, '%Y-%m-%d %H:%M')
            manager.create_event(args.name, args.category, start_time, args.duration)
        except ValueError:
            print("Error: Incorrect date format. Please use 'YYYY-MM-DD HH:MM'.")


                
    if args.update:
        if args.keys:
            if len(args.keys) > 1 and args.start:
                print("Error: Cannot use -start with multiple events.")
                return

            start_times = args.keys
            name = args.name
            category = args.category
            new_start = datetime.strptime(args.start, '%Y-%m-%d %H:%M') if args.start else None

            # Check if the duration is an increment / decrement
            sign = None
            duration = None
            if args.duration:
                if args.duration.startswith('+'):
                    sign = 0 
                    duration = int(args.duration[1:])  # Extract the increment value
                elif args.duration.startswith('-'):
                    sign = 1
                    duration = int(args.duration[1:])  # Extract the decrement value
                else:
                    duration = int(args.duration)

            try:
                manager.update_event(
                    start_times=start_times,
                    name=name,
                    category=category,
                    new_start=new_start if len(start_times) == 1 else None,  # Only allow new_start if there's one key
                    duration=duration,
                    sign=sign
                )
            except ValueError as e:
                print(e)
        else:
            print("Error: Missing required -keys argument to specify which event(s) to update.")


            
    elif args.delete:
        if not args.start:
            print("Error: Missing required argument -start to identify the event to delete.")
            print("Usage: -delete -start 'YYYY-MM-DD HH:MM'")
            return

        manager.delete_event(args.start)
        print("Event deleted successfully.")

    elif args.list:
        events = manager.list_events()
        if events:
            for key, event in events.items():
                print(f"Time: {key}, Name: {event[0]}, Category: {event[1]}, Duration: {event[3]} minutes")
        else:
            print("No events scheduled.")

    elif args.filter:
        if args.category:
                # Use the generator to filter events by category
            filtered_events = manager.filter_events_by_category(args.category)
            found = False  # Flag to check if any events are found
            for key, event in filtered_events:
                print(f"Time: {key}, Name: {event[0]}, Category: {event[1]}, Duration: {event[3]} minutes")
                found = True
            if not found:
                print(f"No events found for the category: {args.category}")
        else:
            print("Error: Missing required argument -category to specify which category to filter.")


    elif args.report:
        manager.generate_report()

if __name__ == '__main__':
    main()
