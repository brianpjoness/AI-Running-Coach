# AI Running Training Plan Generator

A scientific, evidence-based training plan generator that follows the principles outlined in the `.cursorrules` file, including periodization, progressive overload, and injury prevention.

## 🏃‍♀️ Features

- **Scientific Foundation**: Based on peer-reviewed research and coaching principles
- **80/20 Polarized Training**: Follows the proven 80% easy, 20% hard training model
- **Periodization**: Implements Base → Build → Peak → Taper progression
- **Individual Customization**: Adapts to experience level, target distance, and preferences
- **Injury Prevention**: Built-in 10% rule and recovery week scheduling
- **Multiple Distances**: Supports 1 Mile, 5K, 10K, Half Marathon, and Marathon training

## 🧬 Scientific Principles

### Training Zones & Intensity Distribution
- **Zone 1-2 (80% of training)**: Aerobic base development, fat oxidation
- **Zone 4-5 (20% of training)**: VO2 max and lactate threshold development
- **Zone 3 (minimized)**: The "gray zone" - too hard for easy days, too easy for hard days

### Periodization Model
- **Base Phase**: Aerobic foundation, musculoskeletal durability
- **Build Phase**: Increasing training stress, race-specific preparation
- **Peak Phase**: Race-specific training, performance optimization
- **Taper Phase**: Volume reduction, performance peaking

### Injury Prevention
- **10% Rule**: Maximum weekly mileage increase
- **Recovery Weeks**: Scheduled every 3-5 weeks based on experience level
- **Progressive Overload**: Systematic training stress progression
- **Strength Training**: Integrated 2-3 times per week

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd RunningCoachAI

# No external dependencies required!
python main.py
```

### Basic Usage

```python
from datetime import date
from src.models import RunnerProfile, RaceDistance, ExperienceLevel
from src.plan_generator import TrainingPlanGenerator
from src.formatter import TrainingPlanFormatter

# Create runner profile
profile = RunnerProfile(
    experience_level=ExperienceLevel.INTERMEDIATE,
    target_distance=RaceDistance.HALF_MARATHON,
    peak_race_date=date(2024, 6, 15),
    weekly_mileage_target=35,
    days_per_week=5
)

# Generate training plan
generator = TrainingPlanGenerator()
plan = generator.generate_plan(profile)

# Format and display
formatter = TrainingPlanFormatter()
print(formatter.format_plan_summary(plan))
```

### Interactive Mode

```bash
python main.py
```

Follow the prompts to create your personalized training plan.

### Example Plans

```bash
python main.py examples
```

View example training plans for different distances and experience levels.

## 📊 Supported Distances

| Distance | Training Weeks | Key Focus | Energy System |
|----------|----------------|-----------|---------------|
| 1 Mile | 8-12 weeks | Neuromuscular power | 85% aerobic, 15% anaerobic |
| 5K | 10-16 weeks | VO2 max development | 92.5% aerobic, 7.5% anaerobic |
| 10K | 12-18 weeks | Lactate threshold | 96% aerobic, 4% anaerobic |
| Half Marathon | 14-20 weeks | Aerobic threshold | 97.5% aerobic, 2.5% anaerobic |
| Marathon | 16-24 weeks | Metabolic efficiency | 98.5% aerobic, 1.5% anaerobic |

## 🎯 Experience Level Adjustments

### Beginner (< 1 year running)
- **Mileage Increase**: 5% weekly (conservative)
- **Max Mileage**: 80% of target
- **Recovery Weeks**: Every 3rd week
- **Base Phase**: +2 weeks extension

### Intermediate (1-3 years running)
- **Mileage Increase**: 8% weekly
- **Max Mileage**: 90% of target
- **Recovery Weeks**: Every 4th week
- **Base Phase**: +1 week extension

### Advanced (3+ years running)
- **Mileage Increase**: 10% weekly
- **Max Mileage**: 100% of target
- **Recovery Weeks**: Every 5th week
- **Base Phase**: Standard duration

## 📋 Training Plan Structure

### Weekly Schedule
- **Long Run**: 15-35% of weekly mileage (distance-dependent)
- **Easy Runs**: 60-80% of weekly mileage
- **Quality Sessions**: 20% of weekly mileage (tempo, intervals, hills)
- **Rest Days**: Integrated based on training days preference

### Workout Types
- **Easy Run**: Conversational pace, Zone 2
- **Long Run**: Steady pace, Zone 2, practice nutrition
- **Tempo Run**: Lactate threshold pace, Zone 4
- **Intervals**: VO2 max development, Zone 5
- **Strides**: Neuromuscular coordination, Zone 4
- **Hills**: Strength and form, Zone 4
- **Race Pace**: Specific pace practice, Zone 4
- **Recovery**: Very easy pace, Zone 1
- **Rest**: Complete rest or light activity

## 💪 Strength Training Integration

### Recommended Frequency
- **Beginner**: 2 days per week
- **Intermediate**: 2 days per week
- **Advanced**: 3 days per week

### Focus Areas
- Hip abductors and extensors
- Core stability
- Single-leg exercises
- Posterior chain strengthening

### Timing
- On non-running days
- After easy runs
- Before quality sessions (light activation)

## 🔄 Recovery & Adaptation

### Recovery Guidelines
- **Sleep**: 8+ hours per night
- **Nutrition**: Post-workout within 30-60 minutes
- **Active Recovery**: Light movement preferred over complete rest
- **Monitoring**: Track resting heart rate, sleep quality, energy levels

### Adaptation Timeline
- **Cardiovascular**: 1-4 weeks
- **Mitochondrial**: 4-8 weeks
- **Metabolic**: 8-12 weeks
- **Supercompensation**: 7-day cycle

## 📁 Project Structure

```
RunningCoachAI/
├── main.py                 # Main application entry point
├── requirements.txt        # Dependencies (minimal)
├── README.md              # This file
├── .cursorrules           # Scientific principles and coding guidelines
└── src/
    ├── __init__.py        # Package initialization
    ├── models.py          # Data models and enums
    ├── config.py          # Training configurations
    ├── plan_generator.py  # Core training plan generation logic
    └── formatter.py       # Plan formatting and export
```

## 🧪 Scientific References

The training principles implemented in this generator are based on:

1. **Polarized Training Model**: Seiler & Tønnessen (2009)
2. **Periodization**: Bompa & Haff (2009)
3. **Injury Prevention**: Nielsen et al. (2012)
4. **Recovery Science**: Kellmann & Beckmann (2018)
5. **Distance-Specific Training**: Daniels (2013)

## 🤝 Contributing

This project follows the coding guidelines outlined in `.cursorrules`:

- Prefer simple solutions
- Avoid code duplication
- Keep files under 200-300 lines
- Follow scientific principles
- Maintain clean, organized codebase

## 📄 License

This project is designed for educational and personal use. The scientific principles are based on established research in exercise physiology and coaching methodology.

## 🆘 Support

For questions or issues:
1. Check the example plans: `python main.py examples`
2. Review the help: `python main.py help`
3. Examine the scientific principles in `.cursorrules`

---

**Disclaimer**: This training plan generator provides general guidance based on scientific principles. Individual responses to training vary, and runners should consult with healthcare professionals before beginning any training program, especially if they have pre-existing medical conditions.