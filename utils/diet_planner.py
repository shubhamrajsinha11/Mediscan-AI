"""
Personalized Diet Planning Module
Generates custom meal plans based on disease
"""

import random

class DietPlanner:
    def __init__(self):
        self.diet_database = self.create_diet_database()
    
    def create_diet_database(self):
        """Create comprehensive diet database for various diseases"""
        return {
            'common cold': {
                'foods_to_eat': [
                    'Chicken soup', 'Ginger tea', 'Honey', 'Citrus fruits (oranges, lemons)',
                    'Garlic', 'Green leafy vegetables', 'Yogurt', 'Oatmeal', 'Bananas',
                    'Whole grains', 'Lean proteins', 'Warm fluids'
                ],
                'foods_to_avoid': [
                    'Dairy products (may increase mucus)', 'Sugary foods', 'Processed foods',
                    'Fried foods', 'Alcohol', 'Caffeine (in excess)'
                ],
                'breakfast': [
                    'Oatmeal with honey and banana',
                    'Scrambled eggs with whole grain toast',
                    'Yogurt with berries and honey',
                    'Warm ginger tea with lemon'
                ],
                'lunch': [
                    'Chicken soup with vegetables',
                    'Grilled chicken with steamed vegetables',
                    'Vegetable broth with whole grain crackers',
                    'Quinoa salad with lean protein'
                ],
                'dinner': [
                    'Baked fish with steamed vegetables',
                    'Lentil soup with whole grain bread',
                    'Chicken and vegetable stir-fry',
                    'Vegetable curry with brown rice'
                ],
                'snacks': [
                    'Fresh fruits (oranges, apples)',
                    'Nuts and seeds',
                    'Yogurt',
                    'Herbal tea with honey'
                ]
            },
            'fever': {
                'foods_to_eat': [
                    'Clear broths', 'Coconut water', 'Electrolyte drinks', 'Bananas',
                    'Rice', 'Applesauce', 'Toast', 'Ginger tea', 'Honey', 'Plain yogurt',
                    'Boiled vegetables', 'Lean proteins'
                ],
                'foods_to_avoid': [
                    'Heavy, fatty foods', 'Spicy foods', 'Dairy (if causing issues)',
                    'Raw vegetables', 'Alcohol', 'Caffeine'
                ],
                'breakfast': [
                    'Plain toast with honey',
                    'Oatmeal with banana',
                    'Scrambled eggs (if tolerated)',
                    'Herbal tea'
                ],
                'lunch': [
                    'Clear vegetable broth',
                    'Boiled rice with plain chicken',
                    'Steamed vegetables',
                    'Applesauce'
                ],
                'dinner': [
                    'Chicken soup',
                    'Boiled vegetables with rice',
                    'Plain pasta with minimal sauce',
                    'Steamed fish'
                ],
                'snacks': [
                    'Bananas',
                    'Coconut water',
                    'Plain crackers',
                    'Herbal tea'
                ]
            },
            'diarrhea': {
                'foods_to_eat': [
                    'Bananas', 'Rice', 'Applesauce', 'Toast (BRAT diet)',
                    'Boiled potatoes', 'Plain crackers', 'Chicken (boiled)',
                    'Yogurt (with probiotics)', 'Coconut water', 'Clear broths'
                ],
                'foods_to_avoid': [
                    'Dairy products (except yogurt)', 'Fried foods', 'Spicy foods',
                    'High-fiber foods', 'Caffeine', 'Alcohol', 'Sugary foods',
                    'Raw vegetables', 'Beans and legumes'
                ],
                'breakfast': [
                    'Banana and plain toast',
                    'Rice porridge',
                    'Applesauce',
                    'Plain crackers'
                ],
                'lunch': [
                    'Boiled rice with plain chicken',
                    'Chicken soup',
                    'Boiled potatoes',
                    'Plain pasta'
                ],
                'dinner': [
                    'Steamed fish with rice',
                    'Boiled vegetables and chicken',
                    'Plain rice with boiled eggs',
                    'Chicken broth'
                ],
                'snacks': [
                    'Bananas',
                    'Plain crackers',
                    'Applesauce',
                    'Coconut water'
                ]
            },
            'headache': {
                'foods_to_eat': [
                    'Water (hydration)', 'Magnesium-rich foods (spinach, almonds)',
                    'Ginger', 'Peppermint tea', 'Whole grains', 'Lean proteins',
                    'Fresh fruits', 'Vegetables', 'Nuts and seeds'
                ],
                'foods_to_avoid': [
                    'Processed foods', 'Aged cheeses', 'Chocolate', 'Alcohol',
                    'Caffeine (in excess)', 'Artificial sweeteners', 'MSG',
                    'Nitrates (processed meats)'
                ],
                'breakfast': [
                    'Oatmeal with almonds and berries',
                    'Whole grain toast with avocado',
                    'Smoothie with spinach and banana',
                    'Greek yogurt with fruits'
                ],
                'lunch': [
                    'Grilled chicken salad',
                    'Quinoa bowl with vegetables',
                    'Lentil soup',
                    'Salmon with steamed vegetables'
                ],
                'dinner': [
                    'Baked fish with vegetables',
                    'Chicken stir-fry with brown rice',
                    'Vegetable curry',
                    'Lean protein with sweet potato'
                ],
                'snacks': [
                    'Almonds',
                    'Fresh fruits',
                    'Peppermint tea',
                    'Dark chocolate (in moderation)'
                ]
            },
            'cough': {
                'foods_to_eat': [
                    'Honey', 'Ginger tea', 'Turmeric', 'Garlic', 'Warm fluids',
                    'Chicken soup', 'Citrus fruits', 'Green leafy vegetables',
                    'Yogurt', 'Whole grains'
                ],
                'foods_to_avoid': [
                    'Dairy (may increase phlegm)', 'Sugary foods', 'Cold foods',
                    'Fried foods', 'Processed foods'
                ],
                'breakfast': [
                    'Oatmeal with honey',
                    'Scrambled eggs with toast',
                    'Yogurt with fruits',
                    'Ginger tea'
                ],
                'lunch': [
                    'Chicken soup',
                    'Steamed vegetables with rice',
                    'Lentil soup',
                    'Grilled chicken salad'
                ],
                'dinner': [
                    'Baked fish with vegetables',
                    'Chicken and vegetable soup',
                    'Vegetable curry',
                    'Steamed vegetables with quinoa'
                ],
                'snacks': [
                    'Honey and lemon tea',
                    'Fresh fruits',
                    'Nuts',
                    'Warm herbal tea'
                ]
            },
            'nausea': {
                'foods_to_eat': [
                    'Ginger', 'Crackers', 'Bananas', 'Rice', 'Applesauce',
                    'Toast', 'Clear broths', 'Peppermint tea', 'Lemon',
                    'Plain yogurt'
                ],
                'foods_to_avoid': [
                    'Spicy foods', 'Fried foods', 'Heavy, fatty foods',
                    'Strong-smelling foods', 'Dairy (if causing issues)',
                    'Caffeine', 'Alcohol'
                ],
                'breakfast': [
                    'Plain toast or crackers',
                    'Ginger tea',
                    'Banana',
                    'Plain oatmeal'
                ],
                'lunch': [
                    'Clear broth',
                    'Boiled rice',
                    'Plain chicken',
                    'Applesauce'
                ],
                'dinner': [
                    'Steamed vegetables with rice',
                    'Plain pasta',
                    'Boiled chicken',
                    'Clear soup'
                ],
                'snacks': [
                    'Ginger tea',
                    'Crackers',
                    'Bananas',
                    'Peppermint tea'
                ]
            },
            'pain': {
                'foods_to_eat': [
                    'Anti-inflammatory foods (turmeric, ginger)', 'Omega-3 rich foods (fish)',
                    'Green leafy vegetables', 'Berries', 'Nuts', 'Whole grains',
                    'Lean proteins', 'Olive oil'
                ],
                'foods_to_avoid': [
                    'Processed foods', 'Sugary foods', 'Fried foods',
                    'Red meat (in excess)', 'Alcohol', 'Refined carbs'
                ],
                'breakfast': [
                    'Oatmeal with berries and nuts',
                    'Smoothie with spinach and fruits',
                    'Whole grain toast with avocado',
                    'Greek yogurt with fruits'
                ],
                'lunch': [
                    'Salmon salad',
                    'Quinoa bowl with vegetables',
                    'Lentil soup',
                    'Grilled chicken with vegetables'
                ],
                'dinner': [
                    'Baked fish with vegetables',
                    'Chicken with sweet potato',
                    'Vegetable curry',
                    'Lean protein with quinoa'
                ],
                'snacks': [
                    'Nuts and seeds',
                    'Fresh fruits',
                    'Yogurt',
                    'Herbal tea'
                ]
            },
            'allergy': {
                'foods_to_eat': [
                    'Anti-inflammatory foods', 'Probiotics (yogurt, kefir)',
                    'Quercetin-rich foods (apples, onions)', 'Omega-3 foods',
                    'Vitamin C rich foods', 'Green leafy vegetables',
                    'Local honey (if not allergic)'
                ],
                'foods_to_avoid': [
                    'Known allergens', 'Processed foods', 'Foods with additives',
                    'Alcohol', 'Dairy (if allergic)', 'Nuts (if allergic)'
                ],
                'breakfast': [
                    'Oatmeal with fruits',
                    'Smoothie with spinach',
                    'Whole grain toast',
                    'Yogurt with berries'
                ],
                'lunch': [
                    'Grilled chicken salad',
                    'Quinoa bowl',
                    'Vegetable soup',
                    'Salmon with vegetables'
                ],
                'dinner': [
                    'Baked fish',
                    'Chicken with vegetables',
                    'Vegetable curry',
                    'Lean protein with rice'
                ],
                'snacks': [
                    'Fresh fruits',
                    'Nuts (if not allergic)',
                    'Yogurt',
                    'Vegetable sticks'
                ]
            }
        }
    
    def generate_meal_plan(self, disease, days=7, symptoms=None):
        """Generate personalized meal plan for a disease with unique meals for each day"""
        disease_lower = disease.lower()
        
        # Find matching diet plan
        diet_plan = None
        for key in self.diet_database:
            if key in disease_lower or disease_lower in key:
                diet_plan = self.diet_database[key].copy()
                break
        
        # Default plan if not found
        if diet_plan is None:
            diet_plan = {
                'foods_to_eat': [
                    'Fresh fruits and vegetables', 'Whole grains', 'Lean proteins',
                    'Healthy fats', 'Adequate hydration', 'Probiotics'
                ],
                'foods_to_avoid': [
                    'Processed foods', 'Sugary foods', 'Excessive caffeine',
                    'Alcohol', 'Fried foods'
                ],
                'breakfast': ['Balanced breakfast with protein and whole grains'],
                'lunch': ['Nutritious lunch with vegetables and lean protein'],
                'dinner': ['Light, healthy dinner'],
                'snacks': ['Healthy snacks like fruits or nuts']
            }
        
        # Adjust plan based on symptoms if provided
        if symptoms:
            symptoms_lower = [s.lower() for s in symptoms]
            if any(s in ['fever', 'high fever'] for s in symptoms_lower):
                # Add more hydration and easy-to-digest foods
                diet_plan['foods_to_eat'].extend(['Clear broths', 'Coconut water', 'Electrolyte drinks'])
            if any(s in ['diarrhea', 'nausea', 'vomiting'] for s in symptoms_lower):
                # Focus on BRAT diet
                diet_plan['breakfast'] = ['Banana and plain toast', 'Rice porridge', 'Applesauce', 'Plain crackers']
                diet_plan['lunch'] = ['Boiled rice with plain chicken', 'Chicken soup', 'Boiled potatoes']
                diet_plan['dinner'] = ['Steamed fish with rice', 'Boiled vegetables and chicken', 'Plain rice']
            if any(s in ['cough', 'sore throat'] for s in symptoms_lower):
                # Add soothing foods
                diet_plan['foods_to_eat'].extend(['Honey', 'Ginger tea', 'Warm fluids'])
        
        # Generate unique daily meal plans with time-based variety
        meal_plans = []
        used_combinations = set()
        
        # Expand meal options for variety
        breakfast_list = diet_plan['breakfast'] * 3 if len(diet_plan['breakfast']) > 0 else ['Balanced breakfast']
        lunch_list = diet_plan['lunch'] * 3 if len(diet_plan['lunch']) > 0 else ['Nutritious lunch']
        dinner_list = diet_plan['dinner'] * 3 if len(diet_plan['dinner']) > 0 else ['Light dinner']
        snacks_list = diet_plan['snacks'] * 3 if len(diet_plan['snacks']) > 0 else ['Healthy snacks']
        
        # Time-based meal suggestions
        time_based_meals = {
            'morning': {
                'breakfast': ['Oatmeal with fruits', 'Scrambled eggs with toast', 'Yogurt with granola', 
                             'Smoothie bowl', 'Whole grain pancakes', 'Avocado toast'],
                'snacks': ['Fresh fruits', 'Nuts', 'Greek yogurt', 'Energy bar']
            },
            'afternoon': {
                'lunch': ['Grilled chicken salad', 'Quinoa bowl', 'Vegetable soup', 
                         'Pasta with vegetables', 'Rice bowl', 'Wrap with lean protein'],
                'snacks': ['Trail mix', 'Apple with peanut butter', 'Vegetable sticks', 'Hummus']
            },
            'evening': {
                'dinner': ['Baked fish with vegetables', 'Stir-fry', 'Soup and salad', 
                          'Grilled vegetables', 'Lean protein with sides', 'Vegetable curry'],
                'snacks': ['Herbal tea', 'Light crackers', 'Fruit', 'Warm milk']
            }
        }
        
        # Adjust meals based on symptoms
        if symptoms:
            symptoms_lower = [s.lower() for s in symptoms]
            if any(s in ['fever', 'high fever'] for s in symptoms_lower):
                # Light, easy-to-digest meals
                breakfast_list = ['Plain toast', 'Oatmeal', 'Banana', 'Herbal tea']
                lunch_list = ['Clear broth', 'Steamed vegetables', 'Rice porridge', 'Applesauce']
                dinner_list = ['Chicken soup', 'Boiled vegetables', 'Plain pasta', 'Steamed fish']
            elif any(s in ['diarrhea', 'nausea'] for s in symptoms_lower):
                # BRAT diet focus
                breakfast_list = ['Banana', 'Plain toast', 'Rice porridge', 'Crackers']
                lunch_list = ['Boiled rice', 'Chicken soup', 'Boiled potatoes', 'Applesauce']
                dinner_list = ['Steamed fish', 'Boiled vegetables', 'Plain rice', 'Chicken broth']
            elif any(s in ['cough', 'sore throat'] for s in symptoms_lower):
                # Soothing foods
                breakfast_list = ['Warm oatmeal', 'Honey tea', 'Soft scrambled eggs', 'Yogurt']
                lunch_list = ['Chicken soup', 'Warm broth', 'Steamed vegetables', 'Soft pasta']
                dinner_list = ['Warm soup', 'Steamed fish', 'Mashed vegetables', 'Soft rice']
        
        for day in range(days):
            # Ensure variety by avoiding exact same combinations
            max_attempts = 50
            attempt = 0
            while attempt < max_attempts:
                # Select meals with variety
                breakfast = random.choice(breakfast_list)
                lunch = random.choice(lunch_list)
                dinner = random.choice(dinner_list)
                
                # Time-appropriate snacks
                morning_snack = random.choice(time_based_meals['morning']['snacks'])
                afternoon_snack = random.choice(time_based_meals['afternoon']['snacks'])
                evening_snack = random.choice(time_based_meals['evening']['snacks'])
                
                combo = (breakfast, lunch, dinner, morning_snack, afternoon_snack, evening_snack)
                if combo not in used_combinations or attempt == max_attempts - 1:
                    used_combinations.add(combo)
                    daily_plan = {
                        'day': day + 1,
                        'breakfast': breakfast,
                        'morning_snack': morning_snack,
                        'lunch': lunch,
                        'afternoon_snack': afternoon_snack,
                        'dinner': dinner,
                        'evening_snack': evening_snack
                    }
                    meal_plans.append(daily_plan)
                    break
                attempt += 1
        
        alternative_meals = {
            'breakfast': sorted(set(breakfast_list))[:5],
            'lunch': sorted(set(lunch_list))[:5],
            'dinner': sorted(set(dinner_list))[:5],
            'snacks': sorted(set(time_based_meals['morning']['snacks'] + time_based_meals['afternoon']['snacks'] + time_based_meals['evening']['snacks']))[:6]
        }
        
        return {
            'foods_to_eat': diet_plan['foods_to_eat'],
            'foods_to_avoid': diet_plan['foods_to_avoid'],
            'daily_plans': meal_plans,
            'alternative_meals': alternative_meals,
            'general_tips': [
                'Stay hydrated throughout the day',
                'Eat smaller, frequent meals if needed',
                'Listen to your body and adjust portions',
                'Include variety for balanced nutrition',
                f'This is a {days}-day personalized meal plan based on your condition'
            ]
        }
    
    def get_simple_recipe(self, meal_type, disease):
        """Get multiple simple recipe suggestions"""
        recipes = {
            'breakfast': {
                'common cold': [
                    'Ginger Honey Tea + whole grain toast',
                    'Scrambled eggs with spinach and turmeric',
                    'Warm oatmeal with banana, honey, and cinnamon'
                ],
                'fever': [
                    'Plain oatmeal with banana and chia seeds',
                    'Steamed idli with coconut water',
                    'Rice porridge with soft boiled egg'
                ],
                'diarrhea': [
                    'Rice congee with shredded chicken',
                    'Banana smoothie with yogurt',
                    'Plain toast with nut butter and banana'
                ]
            },
            'lunch': {
                'common cold': [
                    'Chicken soup with carrots, celery, and ginger',
                    'Quinoa bowl with steamed veggies and lean protein',
                    'Brown rice with lentil stew and greens'
                ],
                'fever': [
                    'Clear vegetable broth with soft rice',
                    'Steamed fish with mashed sweet potato',
                    'Boiled rice with turmeric-spiced lentils'
                ],
                'diarrhea': [
                    'Plain boiled rice with grilled chicken and broth',
                    'Mashed potatoes with steamed carrots',
                    'Soft rice noodles with clear chicken broth'
                ]
            },
            'dinner': {
                'common cold': [
                    'Steamed vegetables with baked salmon',
                    'Warm barley soup with herbs',
                    'Whole wheat roti with vegetable korma'
                ],
                'fever': [
                    'Light vegetable soup with soft tofu',
                    'Plain pasta with olive oil and herbs',
                    'Steamed vegetables with turmeric rice'
                ],
                'diarrhea': [
                    'Steamed fish with plain rice and broth',
                    'Baked sweet potato with spinach puree',
                    'Chicken broth with soft noodles'
                ]
            }
        }
        
        disease_lower = disease.lower()
        matched_recipes = []
        for key, suggestions in recipes.get(meal_type, {}).items():
            if key in disease_lower or disease_lower in key:
                matched_recipes.extend(suggestions)
        
        if not matched_recipes:
            general = {
                'breakfast': [
                    'Greek yogurt parfait with berries',
                    'Smoothie bowl with spinach, banana, and seeds',
                    'Whole grain toast with avocado and poached egg'
                ],
                'lunch': [
                    'Grilled chicken salad with olive oil dressing',
                    'Vegetable stir-fry with tofu and brown rice',
                    'Quinoa tabbouleh with chickpeas'
                ],
                'dinner': [
                    'Baked salmon with steamed asparagus',
                    'Vegetable soup with whole grain roll',
                    'Stuffed bell peppers with lean turkey'
                ]
            }
            matched_recipes = general.get(meal_type, ['Prepare a light, balanced meal.'])
        
        if isinstance(matched_recipes, str):
            matched_recipes = [matched_recipes]
        
        unique_recipes = []
        for recipe in matched_recipes:
            if recipe not in unique_recipes:
                unique_recipes.append(recipe)
        
        return unique_recipes
    
    def get_exercise_suggestions(self, disease, symptoms=None):
        """Provide exercise routine ideas aligned with diet plans"""
        disease_lower = disease.lower()
        suggestions = [
            "Morning breathing exercises (5 minutes) before breakfast.",
            "Gentle shoulder and neck stretches after work.",
            "Short evening walk (10-15 minutes) to aid digestion."
        ]
        
        disease_specific = {
            'common cold': [
                "Steam inhalation followed by light stretching.",
                "Indoor tai chi or balance exercises to avoid cold air."
            ],
            'fever': [
                "Prioritize rest; resume mobility with gentle stretching once fever subsides.",
                "Bedside ankle rotations and foot flexes every few hours."
            ],
            'diarrhea': [
                "Avoid strenuous activity; focus on diaphragmatic breathing.",
                "Seated stretching once hydration is stable."
            ],
            'headache': [
                "Neck and shoulder mobility (cat-cow, chin tucks).",
                "10-minute guided relaxation or yoga nidra."
            ],
            'cough': [
                "Chest-opening stretches; avoid outdoor pollution.",
                "Humidifier-assisted deep breathing sessions."
            ],
            'allergy': [
                "Indoor low-impact cardio (stationary cycling).",
                "Sinus drainage yoga poses (supported forward folds)."
            ]
        }
        
        for key, routines in disease_specific.items():
            if key in disease_lower or disease_lower in key:
                suggestions.extend(routines)
                break
        
        if symptoms:
            symptoms_lower = [s.lower() for s in symptoms]
            if any(s in ['fever', 'high fever'] for s in symptoms_lower):
                suggestions = [
                    "Rest-focused routine with only breathing exercises.",
                    "Resume light stretching 48 hours after fever breaks."
                ]
            elif any(s in ['diarrhea', 'nausea'] for s in symptoms_lower):
                suggestions = [
                    "Bedside stretching and frequent rest intervals.",
                    "Once stable, 5-minute mindfulness walks indoors."
                ]
            elif any(s in ['cough', 'sore throat'] for s in symptoms_lower):
                suggestions.append("Add humidified breathing drills twice daily.")
            elif any(s in ['headache'] for s in symptoms_lower):
                suggestions.append("Incorporate eye and temple massage between meals.")
        
        unique_suggestions = []
        for idea in suggestions:
            if idea not in unique_suggestions:
                unique_suggestions.append(idea)
        
        return unique_suggestions[:6]

