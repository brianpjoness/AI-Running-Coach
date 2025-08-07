# RunningCoachAI 🏃‍♂️

An AI-powered fitness coaching system that generates personalized training plans based on user goals, personal records, weekly mileage, and other factors. The system can also modify training plans based on user progress and performance.

## Features

### 🎯 **Personalized Training Plans**
- Generate custom training plans based on user profile
- Support for different goals: distance building, speed improvement, weight loss, general fitness, race preparation
- Experience-level appropriate training (beginner, intermediate, advanced, elite)
- Progressive overload with proper build and taper phases

### 📊 **Progress Tracking**
- Log completed workout sessions
- Track actual vs. planned performance
- Monitor effort levels and pace improvements
- Calculate completion rates and performance trends

### 🤖 **AI-Powered Plan Modification**
- Analyze recent workout performance
- Automatically adjust training plans based on progress
- Reduce intensity if struggling, increase if performing well
- Maintain training consistency and prevent overtraining

### 👤 **User Profile Management**
- Comprehensive user profiles with personal records
- Track injuries, preferences, and training history
- Support for multiple goals and target races
- Experience-based training recommendations

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RunningCoachAI
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## Usage

### Getting Started

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Create a new profile**
   - Select option 2 to create a new profile
   - Enter your personal information (name, age, weight, height)
   - Select your running experience level
   - Enter your current weekly mileage
   - Choose your running goals
   - Optionally add personal records and target races

3. **Generate a training plan**
   - Select option 2 from the main menu
   - Choose plan duration (4-16 weeks)
   - Optionally specify target weekly mileage
   - The AI will generate a personalized plan

4. **Log your workouts**
   - Use option 3 to log completed workout sessions
   - Track actual distance, duration, pace, and effort level
   - Add notes about how the workout felt

5. **Monitor progress**
   - View your training progress with option 4
   - See recent workout sessions and performance trends

6. **Modify your plan**
   - Use option 5 to have the AI adjust your training plan
   - Plans are modified based on your recent performance
   - Adjustments help maintain optimal training load

### Example User Journey

1. **Sarah** is a beginner runner who wants to complete her first 5K
   - Creates profile: 28 years old, beginner level, currently running 5 miles/week
   - Goal: Race preparation for a 5K in 8 weeks
   - AI generates a 8-week plan building from 5 to 15 miles/week

2. **Mike** is an intermediate runner training for a marathon
   - Creates profile: 35 years old, intermediate level, currently running 25 miles/week
   - Goal: Race preparation for a marathon in 16 weeks
   - AI generates a 16-week plan with proper build and taper phases

3. **Lisa** is an advanced runner looking to improve her 10K time
   - Creates profile: 42 years old, advanced level, currently running 40 miles/week
   - Goal: Time improvement for 10K
   - AI generates a plan with more tempo runs and interval training

## Project Structure

```
RunningCoachAI/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/                   # Source code
│   ├── __init__.py        # Package initialization
│   ├── models.py          # Data models and enums
│   ├── database.py        # Database operations
│   ├── ai_coach.py        # AI training plan generation
│   └── cli_interface.py   # Command-line interface
└── venv/                  # Virtual environment (created during setup)
```

## Core Components

### Data Models (`src/models.py`)
- `UserProfile`: User information, goals, personal records
- `TrainingPlan`: Complete training plans with weeks and workouts
- `WorkoutSession`: Completed workout data
- `ProgressMetrics`: Performance tracking metrics

### Database Manager (`src/database.py`)
- SQLite database for data persistence
- CRUD operations for all data models
- Automatic database initialization

### AI Coach (`src/ai_coach.py`)
- Training plan generation algorithms
- Performance analysis and plan modification
- Experience-level appropriate training templates
- Progressive overload and taper calculations

### CLI Interface (`src/cli_interface.py`)
- User-friendly command-line interface
- Profile creation and management
- Training plan generation and viewing
- Workout logging and progress tracking

## Training Plan Features

### Workout Types
- **Easy Run**: Conversational pace, building endurance
- **Tempo Run**: Threshold pace, improving lactate threshold
- **Intervals**: Speed work, improving VO2 max
- **Long Run**: Steady pace, building endurance
- **Recovery**: Very easy pace, active recovery
- **Cross Training**: Alternative activities (cycling, swimming)
- **Rest**: Complete rest or light stretching

### Plan Progression
- **Build Phase** (70% of plan): Gradual mileage increase
- **Peak Phase** (10% of plan): Maximum training load
- **Taper Phase** (20% of plan): Reduced volume, maintained intensity

### Experience Level Adjustments
- **Beginner**: 3-4 workouts/week, focus on consistency
- **Intermediate**: 4-5 workouts/week, balanced training
- **Advanced**: 5-6 workouts/week, specialized training
- **Elite**: 6+ workouts/week, high-volume training

## Future Enhancements

### Planned Features
- **Web Interface**: Modern web UI for better user experience
- **Mobile App**: iOS/Android app for on-the-go tracking
- **Social Features**: Connect with other runners, share achievements
- **Weather Integration**: Adjust training based on weather conditions
- **Injury Prevention**: AI-powered injury risk assessment
- **Nutrition Guidance**: Meal planning and hydration recommendations
- **Race Predictions**: Performance predictions based on training data

### Technical Improvements
- **Machine Learning**: More sophisticated performance analysis
- **API Integration**: Connect with fitness trackers and apps
- **Cloud Storage**: Multi-device synchronization
- **Real-time Coaching**: Instant feedback and adjustments

## Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:
1. Check the documentation in this README
2. Look for existing issues in the repository
3. Create a new issue with detailed information

---

**Happy Running! 🏃‍♂️💪**

*RunningCoachAI - Your AI-powered running companion*