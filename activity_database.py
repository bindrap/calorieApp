#!/usr/bin/env python3
"""
Comprehensive Activity Database
Contains 50+ activities with accurate MET values from scientific research
MET values sourced from: Ainsworth et al. (2011) Compendium of Physical Activities
"""

ACTIVITY_DATABASE = {
    # CARDIO & RUNNING (MET: 6.0-18.0)
    "Running": {
        "light": {"met": 6.0, "description": "Jogging, light pace (< 5 mph)"},
        "moderate": {"met": 9.8, "description": "Running, moderate pace (6-7 mph)"},
        "high": {"met": 14.5, "description": "Running, fast pace (8+ mph)"},
        "tracks": ["distance", "pace", "elevation"],
        "icon": "🏃"
    },
    "Trail Running": {
        "light": {"met": 7.0, "description": "Easy trail, minimal elevation"},
        "moderate": {"met": 10.0, "description": "Moderate trails, some hills"},
        "high": {"met": 16.0, "description": "Steep/technical trails"},
        "tracks": ["distance", "pace", "elevation"],
        "icon": "⛰️"
    },
    "Treadmill Running": {
        "light": {"met": 7.0, "description": "Light jog, flat"},
        "moderate": {"met": 9.8, "description": "Moderate pace, incline"},
        "high": {"met": 14.0, "description": "Fast pace or steep incline"},
        "tracks": ["distance", "pace", "incline"],
        "icon": "🏃"
    },

    # CYCLING (MET: 4.0-16.0)
    "Cycling": {
        "light": {"met": 5.8, "description": "Leisure cycling (< 10 mph)"},
        "moderate": {"met": 8.0, "description": "Moderate effort (12-14 mph)"},
        "high": {"met": 12.0, "description": "Racing or fast pace (16+ mph)"},
        "tracks": ["distance", "pace", "elevation"],
        "icon": "🚴"
    },
    "Mountain Biking": {
        "light": {"met": 7.0, "description": "Easy trails"},
        "moderate": {"met": 10.0, "description": "Moderate terrain"},
        "high": {"met": 14.0, "description": "Steep/technical trails"},
        "tracks": ["distance", "elevation"],
        "icon": "🚵"
    },
    "Stationary Bike": {
        "light": {"met": 5.5, "description": "Light effort"},
        "moderate": {"met": 7.0, "description": "Moderate effort"},
        "high": {"met": 10.5, "description": "Vigorous effort"},
        "tracks": ["distance", "resistance"],
        "icon": "🚴"
    },

    # SWIMMING (MET: 6.0-11.0)
    "Swimming - Freestyle": {
        "light": {"met": 5.8, "description": "Slow pace, recreational"},
        "moderate": {"met": 9.8, "description": "Moderate pace, laps"},
        "high": {"met": 11.0, "description": "Fast pace, competitive"},
        "tracks": ["laps", "distance", "pool_length"],
        "icon": "🏊"
    },
    "Swimming - Backstroke": {
        "light": {"met": 4.8, "description": "Recreational"},
        "moderate": {"met": 7.0, "description": "Moderate effort"},
        "high": {"met": 9.5, "description": "Vigorous effort"},
        "tracks": ["laps", "distance"],
        "icon": "🏊"
    },
    "Swimming - Breaststroke": {
        "light": {"met": 5.3, "description": "Recreational"},
        "moderate": {"met": 8.3, "description": "Moderate effort"},
        "high": {"met": 10.3, "description": "Vigorous effort"},
        "tracks": ["laps", "distance"],
        "icon": "🏊"
    },
    "Swimming - Butterfly": {
        "light": {"met": 8.0, "description": "Moderate effort"},
        "moderate": {"met": 11.0, "description": "Vigorous effort"},
        "high": {"met": 13.8, "description": "All-out effort"},
        "tracks": ["laps", "distance"],
        "icon": "🏊"
    },
    "Water Polo": {
        "light": {"met": 6.0, "description": "Light play"},
        "moderate": {"met": 8.0, "description": "Casual game"},
        "high": {"met": 10.0, "description": "Competitive game"},
        "tracks": ["duration"],
        "icon": "🤽"
    },

    # MARTIAL ARTS & COMBAT (MET: 6.0-12.0)
    "Jiu Jitsu": {
        "light": {"met": 6.0, "description": "Drilling techniques"},
        "moderate": {"met": 8.0, "description": "Light rolling"},
        "high": {"met": 10.3, "description": "Competition rolling"},
        "tracks": ["rounds", "duration"],
        "icon": "🥋"
    },
    "Boxing": {
        "light": {"met": 7.0, "description": "Shadow boxing, bag work"},
        "moderate": {"met": 9.0, "description": "Sparring, moderate intensity"},
        "high": {"met": 12.8, "description": "Competitive sparring"},
        "tracks": ["rounds", "duration"],
        "icon": "🥊"
    },
    "Kickboxing": {
        "light": {"met": 7.0, "description": "Technique practice"},
        "moderate": {"met": 9.0, "description": "Pad work"},
        "high": {"met": 12.0, "description": "Sparring"},
        "tracks": ["rounds"],
        "icon": "🥊"
    },
    "Muay Thai": {
        "light": {"met": 7.0, "description": "Technique training"},
        "moderate": {"met": 9.5, "description": "Pad/bag work"},
        "high": {"met": 12.0, "description": "Sparring/clinch work"},
        "tracks": ["rounds"],
        "icon": "🥊"
    },
    "MMA Training": {
        "light": {"met": 7.0, "description": "Technique drilling"},
        "moderate": {"met": 9.0, "description": "Mixed training"},
        "high": {"met": 11.0, "description": "Live sparring"},
        "tracks": ["rounds"],
        "icon": "🥋"
    },
    "Karate": {
        "light": {"met": 5.0, "description": "Kata practice"},
        "moderate": {"met": 7.0, "description": "Sparring drills"},
        "high": {"met": 10.0, "description": "Kumite (competition)"},
        "tracks": ["duration"],
        "icon": "🥋"
    },
    "Taekwondo": {
        "light": {"met": 5.0, "description": "Forms practice"},
        "moderate": {"met": 7.5, "description": "Kicking drills"},
        "high": {"met": 10.0, "description": "Sparring"},
        "tracks": ["duration"],
        "icon": "🥋"
    },
    "Wrestling": {
        "light": {"met": 6.0, "description": "Technique practice"},
        "moderate": {"met": 8.0, "description": "Live wrestling"},
        "high": {"met": 12.0, "description": "Competition intensity"},
        "tracks": ["rounds"],
        "icon": "🤼"
    },

    # STRENGTH TRAINING (MET: 3.0-6.0)
    "Weight Training": {
        "light": {"met": 3.5, "description": "Light weights, many reps"},
        "moderate": {"met": 5.0, "description": "Moderate weights"},
        "high": {"met": 6.0, "description": "Heavy weights, compound lifts"},
        "tracks": ["exercises", "sets", "reps", "weight"],
        "icon": "🏋️"
    },
    "Powerlifting": {
        "light": {"met": 4.0, "description": "Warmup sets"},
        "moderate": {"met": 5.0, "description": "Working sets"},
        "high": {"met": 6.0, "description": "Max effort, low reps"},
        "tracks": ["exercises", "sets", "reps", "weight"],
        "icon": "🏋️"
    },
    "CrossFit": {
        "light": {"met": 6.0, "description": "Skill work"},
        "moderate": {"met": 8.5, "description": "WOD, moderate pace"},
        "high": {"met": 12.0, "description": "MetCon, high intensity"},
        "tracks": ["rounds", "reps"],
        "icon": "💪"
    },
    "Calisthenics": {
        "light": {"met": 4.0, "description": "Easy bodyweight exercises"},
        "moderate": {"met": 5.5, "description": "Push-ups, pull-ups"},
        "high": {"met": 8.0, "description": "Advanced movements, plyometrics"},
        "tracks": ["exercises", "reps"],
        "icon": "🤸"
    },
    "Kettlebell Training": {
        "light": {"met": 4.5, "description": "Light swings, goblet squats"},
        "moderate": {"met": 6.0, "description": "Swings, snatches"},
        "high": {"met": 9.8, "description": "High-intensity kettlebell complex"},
        "tracks": ["exercises", "weight", "reps"],
        "icon": "🏋️"
    },

    # HIIT & CARDIO CLASSES (MET: 8.0-14.0)
    "HIIT": {
        "light": {"met": 8.0, "description": "Moderate intervals"},
        "moderate": {"met": 10.0, "description": "Tabata, burpees"},
        "high": {"met": 12.8, "description": "All-out sprints"},
        "tracks": ["rounds", "intervals"],
        "icon": "⚡"
    },
    "Jump Rope": {
        "light": {"met": 8.0, "description": "Slow pace"},
        "moderate": {"met": 11.0, "description": "Moderate pace, 100-120 skips/min"},
        "high": {"met": 12.3, "description": "Fast pace, double-unders"},
        "tracks": ["duration", "skips"],
        "icon": "🪢"
    },
    "Elliptical": {
        "light": {"met": 4.6, "description": "Low resistance"},
        "moderate": {"met": 5.0, "description": "Moderate resistance"},
        "high": {"met": 8.0, "description": "High resistance, fast pace"},
        "tracks": ["distance", "resistance"],
        "icon": "🏃"
    },
    "Stair Climbing": {
        "light": {"met": 4.0, "description": "Slow pace"},
        "moderate": {"met": 8.0, "description": "Moderate pace"},
        "high": {"met": 15.0, "description": "Running stairs"},
        "tracks": ["floors", "duration"],
        "icon": "🪜"
    },
    "Rowing Machine": {
        "light": {"met": 4.8, "description": "Light effort"},
        "moderate": {"met": 7.0, "description": "Moderate effort"},
        "high": {"met": 12.0, "description": "Vigorous effort, sprints"},
        "tracks": ["distance", "split_time"],
        "icon": "🚣"
    },

    # TEAM SPORTS (MET: 5.0-10.0)
    "Basketball": {
        "light": {"met": 5.0, "description": "Shooting practice"},
        "moderate": {"met": 6.5, "description": "Half-court game"},
        "high": {"met": 8.0, "description": "Full-court game"},
        "tracks": ["duration"],
        "icon": "🏀"
    },
    "Soccer": {
        "light": {"met": 5.0, "description": "Casual play"},
        "moderate": {"met": 7.0, "description": "Recreational game"},
        "high": {"met": 10.0, "description": "Competitive game"},
        "tracks": ["duration"],
        "icon": "⚽"
    },
    "Football": {
        "light": {"met": 5.0, "description": "Touch football"},
        "moderate": {"met": 6.0, "description": "Flag football"},
        "high": {"met": 8.0, "description": "Tackle football"},
        "tracks": ["duration"],
        "icon": "🏈"
    },
    "Volleyball": {
        "light": {"met": 3.0, "description": "Recreational, non-competitive"},
        "moderate": {"met": 4.0, "description": "Casual game"},
        "high": {"met": 6.0, "description": "Beach volleyball, competitive"},
        "tracks": ["duration"],
        "icon": "🏐"
    },
    "Tennis": {
        "light": {"met": 5.0, "description": "Doubles, recreational"},
        "moderate": {"met": 7.3, "description": "Singles, moderate"},
        "high": {"met": 8.0, "description": "Singles, competitive"},
        "tracks": ["duration", "sets"],
        "icon": "🎾"
    },
    "Badminton": {
        "light": {"met": 4.5, "description": "Recreational"},
        "moderate": {"met": 5.5, "description": "Social game"},
        "high": {"met": 7.0, "description": "Competitive"},
        "tracks": ["duration"],
        "icon": "🏸"
    },
    "Hockey": {
        "light": {"met": 5.0, "description": "Practice"},
        "moderate": {"met": 8.0, "description": "Recreational game"},
        "high": {"met": 10.0, "description": "Competitive game"},
        "tracks": ["duration"],
        "icon": "🏒"
    },
    "Rugby": {
        "light": {"met": 6.0, "description": "Touch rugby"},
        "moderate": {"met": 8.0, "description": "Practice"},
        "high": {"met": 10.0, "description": "Full-contact game"},
        "tracks": ["duration"],
        "icon": "🏉"
    },

    # EXTREME SPORTS (MET: 5.0-12.0)
    "Skateboarding": {
        "light": {"met": 5.0, "description": "Cruising, flat ground"},
        "moderate": {"met": 6.0, "description": "Street skating, tricks"},
        "high": {"met": 9.0, "description": "Vert ramp, aggressive skating"},
        "tracks": ["duration", "distance", "tricks_landed"],
        "icon": "🛹"
    },
    "Surfing": {
        "light": {"met": 3.0, "description": "Lying on board"},
        "moderate": {"met": 5.0, "description": "Recreational surfing"},
        "high": {"met": 7.0, "description": "Competitive surfing"},
        "tracks": ["duration", "waves_caught"],
        "icon": "🏄"
    },
    "Rock Climbing": {
        "light": {"met": 5.8, "description": "Bouldering, easy routes"},
        "moderate": {"met": 8.0, "description": "Moderate routes"},
        "high": {"met": 11.0, "description": "Difficult routes, lead climbing"},
        "tracks": ["routes", "grade", "height"],
        "icon": "🧗"
    },
    "Snowboarding": {
        "light": {"met": 5.3, "description": "Light effort"},
        "moderate": {"met": 7.0, "description": "Moderate effort"},
        "high": {"met": 8.0, "description": "Vigorous effort"},
        "tracks": ["runs", "duration"],
        "icon": "🏂"
    },
    "Skiing": {
        "light": {"met": 4.3, "description": "Downhill, light effort"},
        "moderate": {"met": 5.3, "description": "Downhill, moderate effort"},
        "high": {"met": 8.0, "description": "Cross-country or racing"},
        "tracks": ["runs", "duration"],
        "icon": "⛷️"
    },
    "BMX": {
        "light": {"met": 6.0, "description": "Casual riding"},
        "moderate": {"met": 8.0, "description": "Park/street riding"},
        "high": {"met": 10.0, "description": "Racing, vert"},
        "tracks": ["duration", "tricks"],
        "icon": "🚴"
    },

    # WATER SPORTS (MET: 3.0-12.0)
    "Kayaking": {
        "light": {"met": 3.0, "description": "Calm water, leisure"},
        "moderate": {"met": 5.0, "description": "Moderate effort"},
        "high": {"met": 12.5, "description": "Whitewater, competitive"},
        "tracks": ["distance", "duration"],
        "icon": "🛶"
    },
    "Stand-up Paddleboarding": {
        "light": {"met": 3.0, "description": "Calm water"},
        "moderate": {"met": 6.0, "description": "Touring"},
        "high": {"met": 8.0, "description": "Racing, waves"},
        "tracks": ["distance", "duration"],
        "icon": "🏄"
    },

    # MIND-BODY (MET: 2.0-4.0)
    "Yoga": {
        "light": {"met": 2.3, "description": "Hatha, gentle"},
        "moderate": {"met": 3.0, "description": "Vinyasa, flow"},
        "high": {"met": 4.0, "description": "Power yoga, Ashtanga"},
        "tracks": ["duration", "style"],
        "icon": "🧘"
    },
    "Pilates": {
        "light": {"met": 3.0, "description": "Mat Pilates"},
        "moderate": {"met": 4.0, "description": "Reformer Pilates"},
        "high": {"met": 5.0, "description": "Advanced Pilates"},
        "tracks": ["duration"],
        "icon": "🧘"
    },
    "Tai Chi": {
        "light": {"met": 1.5, "description": "Gentle movements"},
        "moderate": {"met": 3.0, "description": "Standard practice"},
        "high": {"met": 4.0, "description": "Vigorous practice"},
        "tracks": ["duration"],
        "icon": "🧘"
    },
    "Stretching": {
        "light": {"met": 2.3, "description": "Mild stretching"},
        "moderate": {"met": 3.8, "description": "Active stretching"},
        "high": {"met": 5.0, "description": "Dynamic stretching routine"},
        "tracks": ["duration"],
        "icon": "🤸"
    },

    # WALKING & HIKING (MET: 2.5-7.0)
    "Walking": {
        "light": {"met": 2.8, "description": "Slow pace (< 2 mph)"},
        "moderate": {"met": 3.5, "description": "Moderate pace (3 mph)"},
        "high": {"met": 5.0, "description": "Brisk pace (4+ mph)"},
        "tracks": ["distance", "pace", "steps"],
        "icon": "🚶"
    },
    "Hiking": {
        "light": {"met": 4.8, "description": "Flat terrain, easy trails"},
        "moderate": {"met": 6.5, "description": "Hills, moderate terrain"},
        "high": {"met": 9.0, "description": "Steep, carrying backpack"},
        "tracks": ["distance", "elevation", "duration"],
        "icon": "🥾"
    },

    # DANCING (MET: 3.0-7.8)
    "Dancing": {
        "light": {"met": 3.0, "description": "Slow dancing, ballroom"},
        "moderate": {"met": 4.8, "description": "Social dancing, line dancing"},
        "high": {"met": 7.8, "description": "Aerobic dance, Zumba"},
        "tracks": ["duration", "style"],
        "icon": "💃"
    },

    # MISC ACTIVITIES (MET: 2.5-8.0)
    "Golf": {
        "light": {"met": 3.5, "description": "Using cart"},
        "moderate": {"met": 4.8, "description": "Carrying clubs"},
        "high": {"met": 5.5, "description": "Walking, carrying clubs, hilly"},
        "tracks": ["holes", "duration"],
        "icon": "⛳"
    },
    "Gardening": {
        "light": {"met": 3.0, "description": "Light work"},
        "moderate": {"met": 4.0, "description": "Moderate digging, raking"},
        "high": {"met": 5.0, "description": "Heavy digging, shoveling"},
        "tracks": ["duration"],
        "icon": "🌱"
    },
    "Yard Work": {
        "light": {"met": 3.0, "description": "Raking, bagging"},
        "moderate": {"met": 5.0, "description": "Mowing, trimming"},
        "high": {"met": 6.0, "description": "Chopping wood, heavy lifting"},
        "tracks": ["duration"],
        "icon": "🌳"
    },
}

def get_activity_list():
    """Get list of all activity names"""
    return sorted(ACTIVITY_DATABASE.keys())

def get_activity_info(activity_name):
    """Get MET values and tracking fields for an activity"""
    return ACTIVITY_DATABASE.get(activity_name)

def get_met_value(activity_name, intensity, exertion_rating=None):
    """
    Get MET value for specific activity and intensity

    Args:
        activity_name: Name of activity
        intensity: 'light', 'moderate', or 'high'
        exertion_rating: Optional RPE 1-10 for fine-tuning

    Returns:
        float: MET value
    """
    activity = ACTIVITY_DATABASE.get(activity_name)
    if not activity:
        # Default values if activity not found
        default_mets = {"light": 3.0, "moderate": 5.0, "high": 8.0}
        return default_mets.get(intensity, 5.0)

    base_met = activity[intensity]["met"]

    # Adjust based on exertion if provided
    if exertion_rating:
        if exertion_rating <= 2:
            multiplier = 0.7
        elif exertion_rating <= 4:
            multiplier = 0.9
        elif exertion_rating <= 6:
            multiplier = 1.0
        elif exertion_rating <= 8:
            multiplier = 1.15
        else:  # 9-10
            multiplier = 1.3

        base_met *= multiplier

    return base_met

def get_activities_by_category():
    """Get activities organized by category"""
    categories = {
        "Cardio & Running": [],
        "Cycling": [],
        "Swimming": [],
        "Martial Arts & Combat": [],
        "Strength Training": [],
        "HIIT & Classes": [],
        "Team Sports": [],
        "Extreme Sports": [],
        "Water Sports": [],
        "Mind-Body": [],
        "Walking & Hiking": [],
        "Other": []
    }

    # Categorize based on activity type
    for activity in get_activity_list():
        if "Running" in activity or "Treadmill" in activity:
            categories["Cardio & Running"].append(activity)
        elif "Cycling" in activity or "Bike" in activity or "BMX" in activity:
            categories["Cycling"].append(activity)
        elif "Swimming" in activity or "Water Polo" in activity:
            categories["Swimming"].append(activity)
        elif any(x in activity for x in ["Jiu Jitsu", "Boxing", "MMA", "Karate", "Taekwondo", "Wrestling", "Kickboxing", "Muay Thai"]):
            categories["Martial Arts & Combat"].append(activity)
        elif any(x in activity for x in ["Weight", "Powerlifting", "CrossFit", "Calisthenics", "Kettlebell"]):
            categories["Strength Training"].append(activity)
        elif any(x in activity for x in ["HIIT", "Jump", "Elliptical", "Stair", "Rowing"]):
            categories["HIIT & Classes"].append(activity)
        elif any(x in activity for x in ["Basketball", "Soccer", "Football", "Volleyball", "Tennis", "Badminton", "Hockey", "Rugby"]):
            categories["Team Sports"].append(activity)
        elif any(x in activity for x in ["Skateboarding", "Surfing", "Climbing", "Snowboarding", "Skiing"]):
            categories["Extreme Sports"].append(activity)
        elif any(x in activity for x in ["Kayaking", "Paddleboarding"]):
            categories["Water Sports"].append(activity)
        elif any(x in activity for x in ["Yoga", "Pilates", "Tai Chi", "Stretching"]):
            categories["Mind-Body"].append(activity)
        elif any(x in activity for x in ["Walking", "Hiking"]):
            categories["Walking & Hiking"].append(activity)
        else:
            categories["Other"].append(activity)

    # Remove empty categories
    return {k: v for k, v in categories.items() if v}

if __name__ == "__main__":
    print("=" * 80)
    print("COMPREHENSIVE ACTIVITY DATABASE")
    print("=" * 80)
    print(f"\nTotal Activities: {len(ACTIVITY_DATABASE)}")
    print("\nCategories:")
    for category, activities in get_activities_by_category().items():
        print(f"\n{category} ({len(activities)}):")
        for activity in activities:
            info = get_activity_info(activity)
            print(f"  {info['icon']} {activity}")
            print(f"     Light: {info['light']['met']} MET - {info['light']['description']}")
            print(f"     Moderate: {info['moderate']['met']} MET - {info['moderate']['description']}")
            print(f"     High: {info['high']['met']} MET - {info['high']['description']}")
            if 'tracks' in info:
                print(f"     Tracks: {', '.join(info['tracks'])}")
