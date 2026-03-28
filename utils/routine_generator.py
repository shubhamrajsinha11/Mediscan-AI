"""
Daily Routine Generator
Creates personalized daily schedules based on disease and health metrics
"""

import random
from datetime import datetime, timedelta

class RoutineGenerator:
    def __init__(self):
        self.routine_templates = self.create_routine_templates()
    
    def create_routine_templates(self):
        """Create routine templates for different diseases"""
        return {
            'common cold': {
                'wake_up': '7:00 AM',
                'exercise': 'Light stretching or gentle walk (15-20 min)',
                'hydration': 'Drink water every 1-2 hours',
                'sleep': '9:00 PM - 10:00 PM (8-9 hours)',
                'medication_timing': 'Morning and evening with meals',
                'rest_periods': ['10:00 AM - 10:30 AM', '2:00 PM - 3:00 PM']
            },
            'fever': {
                'wake_up': '8:00 AM',
                'exercise': 'Rest only - no exercise until fever subsides',
                'hydration': 'Drink fluids every 30-60 minutes',
                'sleep': '8:00 PM - 9:00 PM (10-12 hours)',
                'medication_timing': 'Every 4-6 hours as needed',
                'rest_periods': ['Throughout the day - bed rest recommended']
            },
            'diarrhea': {
                'wake_up': '7:30 AM',
                'exercise': 'Light activities only - avoid strenuous exercise',
                'hydration': 'Drink electrolyte solution every 1-2 hours',
                'sleep': '9:30 PM - 10:30 PM (8-9 hours)',
                'medication_timing': 'After meals or as directed',
                'rest_periods': ['11:00 AM - 12:00 PM', '3:00 PM - 4:00 PM']
            },
            'headache': {
                'wake_up': '7:00 AM',
                'exercise': 'Gentle yoga or walking (20-30 min) - avoid if headache is severe',
                'hydration': 'Drink water every hour',
                'sleep': '10:00 PM - 11:00 PM (7-8 hours)',
                'medication_timing': 'At onset of headache, with food',
                'rest_periods': ['12:00 PM - 1:00 PM (lunch break)', '4:00 PM - 4:30 PM']
            },
            'cough': {
                'wake_up': '7:00 AM',
                'exercise': 'Light walking (15-20 min) if tolerated',
                'hydration': 'Warm fluids every 2 hours',
                'sleep': '9:30 PM - 10:30 PM (8-9 hours)',
                'medication_timing': 'Morning and evening, or as directed',
                'rest_periods': ['1:00 PM - 2:00 PM']
            },
            'nausea': {
                'wake_up': '8:00 AM',
                'exercise': 'Very light activities only - rest if severe',
                'hydration': 'Sip fluids slowly throughout the day',
                'sleep': '9:00 PM - 10:00 PM (9-10 hours)',
                'medication_timing': '30 minutes before meals if possible',
                'rest_periods': ['10:00 AM - 11:00 AM', '2:00 PM - 3:00 PM']
            },
            'pain': {
                'wake_up': '7:30 AM',
                'exercise': 'Gentle stretching or light walking (20 min)',
                'hydration': 'Drink water regularly throughout the day',
                'sleep': '10:00 PM - 11:00 PM (7-8 hours)',
                'medication_timing': 'With meals, every 6-8 hours as needed',
                'rest_periods': ['12:00 PM - 1:00 PM', '4:00 PM - 5:00 PM']
            },
            'allergy': {
                'wake_up': '7:00 AM',
                'exercise': 'Indoor exercise preferred, or check pollen levels',
                'hydration': 'Drink water regularly',
                'sleep': '10:00 PM - 11:00 PM (7-8 hours)',
                'medication_timing': 'Morning, with or without food',
                'rest_periods': ['1:00 PM - 2:00 PM']
            }
        }
    
    def generate_routine(self, disease, age=None, bmi=None, temperature=None, wake_preference=None):
        """Generate personalized daily routine"""
        disease_lower = disease.lower()
        
        # Find matching template
        template = None
        for key in self.routine_templates:
            if key in disease_lower or disease_lower in key:
                template = self.routine_templates[key].copy()
                break
        
        # Default template
        if template is None:
            template = {
                'wake_up': '7:00 AM',
                'exercise': 'Light exercise (20-30 min)',
                'hydration': 'Drink water regularly',
                'sleep': '10:00 PM - 11:00 PM (7-8 hours)',
                'medication_timing': 'As directed by healthcare provider',
                'rest_periods': ['1:00 PM - 2:00 PM']
            }
        
        # Adjust based on age
        if age:
            if age < 18:
                template['sleep'] = '9:00 PM - 10:00 PM (9-10 hours)'
                template['exercise'] = 'Age-appropriate activities (30-60 min)'
            elif age > 65:
                template['wake_up'] = '7:30 AM - 8:00 AM'
                template['exercise'] = 'Gentle activities (15-20 min)'
                template['sleep'] = '9:00 PM - 10:00 PM (7-8 hours)'
        
        # Adjust based on temperature (fever)
        if temperature and temperature > 38.0:
            template['exercise'] = 'Rest only - no exercise'
            template['rest_periods'] = ['Throughout the day - bed rest']
        
        # Adjust wake time if preference given
        if wake_preference:
            template['wake_up'] = wake_preference
        
        # Generate detailed schedule
        schedule = self.create_detailed_schedule(template, disease_lower)
        
        return {
            'wake_up': template['wake_up'],
            'exercise': template['exercise'],
            'hydration': template['hydration'],
            'sleep': template['sleep'],
            'medication_timing': template['medication_timing'],
            'rest_periods': template['rest_periods'],
            'detailed_schedule': schedule,
            'tips': self.get_routine_tips(disease_lower, age, bmi, temperature),
            'variation_suggestions': self.get_variation_suggestions(disease_lower)
        }
    
    def create_detailed_schedule(self, template, disease):
        """Create hour-by-hour schedule"""
        wake_time = template['wake_up']
        
        # Parse wake time
        try:
            wake_hour = int(wake_time.split(':')[0])
            wake_min = int(wake_time.split(':')[1].split()[0])
        except:
            wake_hour = 7
            wake_min = 0
        
        schedule = []
        
        # Morning routine
        schedule.append({
            'time': f"{wake_hour:02d}:{wake_min:02d}",
            'activity': 'Wake up',
            'description': 'Start your day with a glass of water'
        })
        
        schedule.append({
            'time': f"{wake_hour:02d}:{wake_min + 30:02d}",
            'activity': 'Medication',
            'description': template['medication_timing']
        })
        
        schedule.append({
            'time': f"{wake_hour + 1:02d}:00",
            'activity': 'Breakfast',
            'description': 'Have a nutritious breakfast'
        })
        
        # Mid-morning
        schedule.append({
            'time': f"{wake_hour + 3:02d}:00",
            'activity': 'Hydration Break',
            'description': template['hydration']
        })
        
        # Exercise time (if applicable)
        if 'no exercise' not in template['exercise'].lower() and 'rest only' not in template['exercise'].lower():
            schedule.append({
                'time': f"{wake_hour + 4:02d}:00",
                'activity': 'Exercise',
                'description': template['exercise']
            })
        
        # Lunch
        schedule.append({
            'time': '12:00',
            'activity': 'Lunch',
            'description': 'Have a balanced lunch'
        })
        
        # Afternoon rest
        if template['rest_periods']:
            schedule.append({
                'time': '1:00 PM',
                'activity': 'Rest Period',
                'description': template['rest_periods'][0] if template['rest_periods'] else 'Take a break'
            })
        
        # Afternoon hydration
        schedule.append({
            'time': '3:00 PM',
            'activity': 'Hydration Break',
            'description': template['hydration']
        })
        
        # Dinner
        schedule.append({
            'time': '7:00 PM',
            'activity': 'Dinner',
            'description': 'Have a light, early dinner'
        })
        
        # Evening medication
        schedule.append({
            'time': '8:00 PM',
            'activity': 'Evening Medication',
            'description': template['medication_timing']
        })
        
        # Sleep
        sleep_time = template['sleep'].split(' - ')[0]
        schedule.append({
            'time': sleep_time,
            'activity': 'Bedtime',
            'description': template['sleep']
        })
        
        return schedule
    
    def get_routine_tips(self, disease, age=None, bmi=None, temperature=None):
        """Get personalized tips for the routine"""
        tips = []
        
        # General tips
        tips.append("Maintain consistent sleep and wake times")
        tips.append("Stay hydrated throughout the day")
        tips.append("Listen to your body and rest when needed")
        
        # Disease-specific tips
        if 'fever' in disease:
            tips.append("Prioritize rest and avoid physical exertion")
            tips.append("Monitor temperature regularly")
        
        if 'diarrhea' in disease:
            tips.append("Focus on hydration with electrolyte solutions")
            tips.append("Avoid heavy meals")
        
        if 'headache' in disease:
            tips.append("Avoid triggers like bright lights and loud noises")
            tips.append("Practice relaxation techniques")
        
        # Age-specific tips
        if age and age > 65:
            tips.append("Take breaks between activities")
            tips.append("Consult healthcare provider before starting new exercises")
        
        # BMI-specific tips
        if bmi:
            if bmi > 30:
                tips.append("Incorporate gradual physical activity")
                tips.append("Focus on balanced nutrition")
            elif bmi < 18.5:
                tips.append("Ensure adequate caloric intake")
                tips.append("Include nutrient-dense foods")
        
        return tips

    def get_variation_suggestions(self, disease):
        """Provide alternative routine ideas for variety"""
        base_variations = [
            "Swap evening walk with restorative yoga or stretching.",
            "Add a 5-minute breathing exercise after lunch.",
            "Include a gratitude journaling session before bed.",
            "Use a standing desk or gentle mobility break mid-afternoon."
        ]
        
        disease_specific = {
            'common cold': [
                "Alternate between herbal tea and infused warm water.",
                "Add steam inhalation before bedtime."
            ],
            'fever': [
                "Replace afternoon rest with lukewarm sponge bath for cooling.",
                "Incorporate guided meditation to support recovery."
            ],
            'diarrhea': [
                "Introduce probiotic snacks in the evening.",
                "Alternate electrolyte drinks with coconut water."
            ],
            'headache': [
                "Schedule a digital detox session in the afternoon.",
                "Use lavender or peppermint aromatherapy before sleep."
            ],
            'cough': [
                "Add humidifier time around bedtime.",
                "Alternate between warm soup and honey-lemon drinks."
            ],
            'allergy': [
                "Rinse nasal passages with saline before sleep.",
                "Plan indoor stretching on high-pollen days."
            ]
        }
        
        variations = base_variations + disease_specific.get(disease, [])
        random.shuffle(variations)
        return variations[:4]

