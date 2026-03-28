"""
Medicine Recommendation Engine
Provides medicine recommendations based on disease
"""

import pandas as pd
import random
import os

class MedicineRecommender:
    def __init__(self):
        self.medicine_map = {}
        self.load_medicine_data()
        self.drug_reviews = {}
        self.condition_statistics = {}
        self.load_drug_reviews()
        self.medicine_database = self.create_medicine_database()
    
    def load_medicine_data(self):
        """Load medicine data from CSV files"""
        try:
            medical_df = pd.read_csv('data/medical data.csv')
            for _, row in medical_df.iterrows():
                disease = str(row.get('Disease', '')).strip().lower()
                medicine = str(row.get('Medicine', '')).strip()
                
                if disease and medicine and disease != 'nan' and medicine != 'nan':
                    if disease not in self.medicine_map:
                        self.medicine_map[disease] = []
                    if medicine not in self.medicine_map[disease]:
                        self.medicine_map[disease].append(medicine)
        except Exception as e:
            print(f"Error loading medicine data: {e}")
    
    def load_drug_reviews(self):
        """Load community-sourced drug reviews for condition mapping"""
        csv_path = 'data/drugsComTest_raw.csv'
        if not os.path.exists(csv_path):
            return
        
        try:
            drugs_df = pd.read_csv(csv_path)
            drugs_df = drugs_df.dropna(subset=['condition', 'drugName'])
            for condition, group in drugs_df.groupby('condition'):
                condition_lower = str(condition).strip().lower()
                entries = []
                for _, row in group.iterrows():
                    drug_name = str(row.get('drugName', '')).strip()
                    rating = row.get('rating', None)
                    review = str(row.get('review', '')).strip()
                    if not drug_name or pd.isna(rating):
                        continue
                    entries.append({
                        'medicine': drug_name,
                        'rating': float(rating),
                        'review': review,
                        'useful_count': int(row.get('usefulCount', 0))
                    })
                
                if entries:
                    # Sort by rating (desc) then usefulness
                    entries.sort(key=lambda x: (x['rating'], x['useful_count']), reverse=True)
                    self.drug_reviews[condition_lower] = entries
                    ratings = [e['rating'] for e in entries]
                    self.condition_statistics[condition_lower] = {
                        'avg_rating': sum(ratings) / len(ratings),
                        'top_medicines': [e['medicine'] for e in entries[:5]]
                    }
        except Exception as e:
            print(f"Error loading drug review data: {e}")
    
    def create_medicine_database(self):
        """Create comprehensive medicine database"""
        return {
            'common cold': {
                'otc': ['Paracetamol', 'Ibuprofen', 'Cetirizine', 'Pseudoephedrine'],
                'prescription': ['Amoxicillin', 'Azithromycin'],
                'natural': ['Honey', 'Ginger Tea', 'Vitamin C', 'Echinacea'],
                'dosage': 'Paracetamol: 500mg every 4-6 hours. Ibuprofen: 200-400mg every 6-8 hours.',
                'age_considerations': 'Children under 12 should use pediatric formulations.',
                'contraindications': 'Avoid if allergic to NSAIDs. Consult doctor if symptoms persist >7 days.'
            },
            'fever': {
                'otc': ['Paracetamol', 'Ibuprofen', 'Aspirin'],
                'prescription': ['Acetaminophen', 'Naproxen'],
                'natural': ['Cool compress', 'Hydration', 'Rest'],
                'dosage': 'Paracetamol: 500-1000mg every 4-6 hours. Maximum 4g/day.',
                'age_considerations': 'Children: Use pediatric dosing. Avoid Aspirin in children.',
                'contraindications': 'Seek immediate medical attention if fever >103°F or persists >3 days.'
            },
            'headache': {
                'otc': ['Paracetamol', 'Ibuprofen', 'Aspirin', 'Caffeine'],
                'prescription': ['Sumatriptan', 'Ergotamine'],
                'natural': ['Peppermint oil', 'Lavender oil', 'Ginger tea', 'Adequate sleep'],
                'dosage': 'Paracetamol: 500-1000mg. Ibuprofen: 200-400mg.',
                'age_considerations': 'Elderly: Lower doses recommended.',
                'contraindications': 'Avoid if severe or sudden onset. Consult for frequent headaches.'
            },
            'cough': {
                'otc': ['Dextromethorphan', 'Guaifenesin', 'Cough drops'],
                'prescription': ['Codeine', 'Benzonatate'],
                'natural': ['Honey', 'Lemon', 'Ginger', 'Thyme tea'],
                'dosage': 'Dextromethorphan: 15-30mg every 4-6 hours.',
                'age_considerations': 'Children under 4: Avoid OTC cough medicines.',
                'contraindications': 'See doctor if cough persists >2 weeks or with blood.'
            },
            'diarrhea': {
                'otc': ['Loperamide', 'Bismuth subsalicylate', 'Oral rehydration salts'],
                'prescription': ['Diphenoxylate', 'Atropine'],
                'natural': ['Probiotics', 'Banana', 'Rice water', 'Ginger'],
                'dosage': 'Loperamide: 2mg after each loose stool, max 8mg/day.',
                'age_considerations': 'Children: Focus on hydration. Consult pediatrician.',
                'contraindications': 'Avoid if bloody diarrhea or fever present. See doctor if >48 hours.'
            },
            'nausea': {
                'otc': ['Dimenhydrinate', 'Meclizine'],
                'prescription': ['Ondansetron', 'Metoclopramide'],
                'natural': ['Ginger', 'Peppermint', 'Lemon', 'Acupressure'],
                'dosage': 'Dimenhydrinate: 50-100mg every 4-6 hours.',
                'age_considerations': 'Pregnant women: Consult doctor before use.',
                'contraindications': 'See doctor if persistent or with severe symptoms.'
            },
            'pain': {
                'otc': ['Paracetamol', 'Ibuprofen', 'Naproxen', 'Aspirin'],
                'prescription': ['Tramadol', 'Codeine', 'Morphine'],
                'natural': ['Turmeric', 'Willow bark', 'Capsaicin cream', 'Arnica'],
                'dosage': 'Ibuprofen: 200-400mg every 6-8 hours. Maximum 1200mg/day.',
                'age_considerations': 'Elderly: Lower doses. Children: Use pediatric formulations.',
                'contraindications': 'Avoid if allergic. Consult for severe or chronic pain.'
            },
            'allergy': {
                'otc': ['Cetirizine', 'Loratadine', 'Diphenhydramine', 'Fexofenadine'],
                'prescription': ['Prednisone', 'Epinephrine'],
                'natural': ['Quercetin', 'Butterbur', 'Probiotics', 'Local honey'],
                'dosage': 'Cetirizine: 10mg once daily.',
                'age_considerations': 'Children: Use pediatric formulations. Elderly: May cause drowsiness.',
                'contraindications': 'Seek immediate help for severe allergic reactions (anaphylaxis).'
            }
        }
    
    def recommend_medicines(self, disease, age=None, symptoms=None):
        """Recommend medicines for a given disease based on symptoms"""
        disease_lower = disease.lower()
        
        # Try exact match first
        if disease_lower in self.medicine_database:
            recommendations = self.medicine_database[disease_lower].copy()
        else:
            # Try partial match
            recommendations = None
            for key in self.medicine_database:
                if key in disease_lower or disease_lower in key:
                    recommendations = self.medicine_database[key].copy()
                    break
            
            # If still not found, use generic recommendations
            if recommendations is None:
                recommendations = {
                    'otc': ['Paracetamol', 'Ibuprofen'],
                    'prescription': ['Consult your doctor for prescription medications'],
                    'natural': ['Rest', 'Hydration', 'Proper nutrition'],
                    'dosage': 'Follow package instructions or consult healthcare provider',
                    'age_considerations': 'Dosage may vary by age. Consult healthcare provider.',
                    'contraindications': 'Always consult a healthcare professional before taking medications.'
                }
        
        # Customize medicines based on specific symptoms
        symptom_context = []
        if symptoms:
            symptoms_lower = [s.lower() for s in symptoms]
            symptom_specific_meds = {
                'fever': {'otc': ['Paracetamol', 'Ibuprofen'], 'natural': ['Cool compress', 'Hydration']},
                'cough': {'otc': ['Dextromethorphan', 'Guaifenesin', 'Cough drops'], 'natural': ['Honey', 'Lemon', 'Ginger tea']},
                'headache': {'otc': ['Paracetamol', 'Ibuprofen', 'Aspirin'], 'natural': ['Peppermint oil', 'Lavender oil', 'Adequate sleep']},
                'diarrhea': {'otc': ['Loperamide', 'Bismuth subsalicylate', 'Oral rehydration salts'], 'natural': ['Probiotics', 'Banana', 'Rice water']},
                'nausea': {'otc': ['Dimenhydrinate', 'Meclizine'], 'natural': ['Ginger', 'Peppermint', 'Lemon']},
                'sore throat': {'otc': ['Lozenges', 'Throat spray', 'Ibuprofen'], 'natural': ['Honey', 'Salt water gargle', 'Warm tea']},
                'runny nose': {'otc': ['Cetirizine', 'Loratadine', 'Pseudoephedrine'], 'natural': ['Steam inhalation', 'Nasal saline']},
                'fatigue': {'otc': [], 'natural': ['Adequate rest', 'B vitamins', 'Iron supplements (if deficient)']},
                'muscle pain': {'otc': ['Ibuprofen', 'Naproxen', 'Topical creams'], 'natural': ['Turmeric', 'Epsom salt bath', 'Massage']},
                'joint pain': {'otc': ['Ibuprofen', 'Naproxen'], 'natural': ['Turmeric', 'Omega-3', 'Warm compress']}
            }
            
            # Add symptom-specific medicines
            for symptom in symptoms_lower:
                for sym_key, meds in symptom_specific_meds.items():
                    if sym_key in symptom or symptom in sym_key:
                        if 'otc' in meds and meds['otc']:
                            recommendations['otc'] = list(set(recommendations.get('otc', []) + meds['otc']))
                        if 'natural' in meds and meds['natural']:
                            recommendations['natural'] = list(set(recommendations.get('natural', []) + meds['natural']))
                        if sym_key in symptom_context:
                            continue
                        symptom_context.append(sym_key)
        
        detail_notes = []
        if 'fever' in symptom_context:
            detail_notes.append("Manage fever symptoms with antipyretics every 4-6 hours and ensure aggressive hydration.")
        if 'cough' in symptom_context or 'sore throat' in symptom_context:
            detail_notes.append("Use expectorants or throat-soothing syrups at night to reduce cough spasms.")
        if 'diarrhea' in symptom_context:
            detail_notes.append("Prioritize oral rehydration salts and BRAT-diet-friendly medications.")
        if 'nausea' in symptom_context:
            detail_notes.append("Take antiemetics 30 minutes before meals to reduce nausea bouts.")
        if symptom_context:
            recommendations['symptom_specific_guidance'] = detail_notes
        
        # Add medicines from CSV data if available
        if disease_lower in self.medicine_map:
            csv_medicines = self.medicine_map[disease_lower]
            if 'otc' in recommendations:
                recommendations['otc'].extend([m for m in csv_medicines if m not in recommendations['otc']])
        
        # Enhance recommendations using community drug reviews (drugsComTest_raw.csv)
        drug_data = self.drug_reviews.get(disease_lower)
        if drug_data:
            community_list = [f"{entry['medicine']} ({entry['rating']}/10)" for entry in drug_data[:5]]
            if community_list:
                recommendations['community_recommended'] = community_list
            
            first_line = [entry['medicine'] for entry in drug_data if entry['rating'] >= 8][:5]
            second_line = [entry['medicine'] for entry in drug_data if 6 <= entry['rating'] < 8][:5]
            adjunct = [entry['medicine'] for entry in drug_data if entry['rating'] < 6][:5]
            
            recommendations['standardized_categories'] = {
                'first_line': first_line or community_list[:3],
                'second_line': second_line,
                'adjunct': adjunct
            }
            
            stats = self.condition_statistics.get(disease_lower, {})
            if stats:
                recommendations['condition_insights'] = (
                    f"Average patient rating: {stats['avg_rating']:.1f}/10. "
                    f"Top community medicines: {', '.join(stats['top_medicines'])}."
                )
            
            if first_line:
                dosage_text = recommendations.get('dosage', '')
                standardized_text = (
                    f" Standard guidance: Follow physician-prescribed dosing for {first_line[0]} "
                    "and monitor patient response. Adjust per standard formularies."
                )
                recommendations['dosage'] = f"{dosage_text}{standardized_text}".strip()
        
        # Remove duplicates while preserving order
        if 'otc' in recommendations:
            seen = set()
            recommendations['otc'] = [x for x in recommendations['otc'] if not (x in seen or seen.add(x))]
        if 'natural' in recommendations:
            seen = set()
            recommendations['natural'] = [x for x in recommendations['natural'] if not (x in seen or seen.add(x))]
        
        combined_for_variety = []
        combined_for_variety.extend(recommendations.get('otc', []))
        combined_for_variety.extend(recommendations.get('prescription', []))
        if combined_for_variety:
            unique_combined = list(dict.fromkeys(combined_for_variety))
            random.shuffle(unique_combined)
            recommendations['variety_options'] = unique_combined[:5]
        
        # Age-specific adjustments
        if age:
            if age < 18:
                recommendations['age_considerations'] = 'Pediatric dosing required. Consult pediatrician.'
            elif age > 65:
                recommendations['age_considerations'] = 'Elderly patients may require dose adjustments. Consult doctor.'
        
        timing_details = []
        if symptom_context:
            if 'fever' in symptom_context:
                timing_details.append("Alternate fever reducers every 4-6 hours, avoiding duplicate NSAIDs.")
            if 'cough' in symptom_context:
                timing_details.append("Prefer sedating cough syrups at night, non-sedating expectorants during the day.")
            if 'diarrhea' in symptom_context or 'nausea' in symptom_context:
                timing_details.append("Take gut-calming medicines 30 minutes before bland meals.")
        if not timing_details:
            timing_details.append("Follow physician-prescribed timing, aligning doses with meals to minimize side-effects.")
        recommendations['medication_timing_detail'] = " ".join(timing_details)
        
        dosage_details = recommendations.get('dosage', '')
        if symptom_context:
            dosage_details += " Adjust dosage based on symptom severity; escalate only under medical supervision."
        recommendations['dosage_detail'] = dosage_details.strip()
        
        contraindication_details = recommendations.get('contraindications', '')
        if 'fever' in symptom_context:
            contraindication_details += " Avoid NSAIDs if there is stomach ulcer history."
        if 'cough' in symptom_context:
            contraindication_details += " Check for drowsiness before driving when using sedating cough syrups."
        recommendations['contraindications_detail'] = contraindication_details.strip()
        
        return recommendations
    
    def get_when_to_see_doctor(self, disease, symptoms_severity='moderate'):
        """Provide guidance on when to see a doctor"""
        general_guidelines = [
            "Symptoms persist for more than 7-10 days",
            "Severe pain or discomfort",
            "High fever (>103°F or 39.4°C)",
            "Difficulty breathing",
            "Signs of dehydration",
            "Symptoms worsen despite treatment",
            "Pregnancy or underlying health conditions"
        ]
        
        disease_specific = {
            'fever': ["Fever >103°F", "Fever lasts >3 days", "Rash appears"],
            'cough': ["Cough with blood", "Cough lasts >2 weeks", "Shortness of breath"],
            'diarrhea': ["Bloody stools", "Severe dehydration", "Lasts >48 hours"],
            'headache': ["Sudden severe headache", "Headache with vision changes", "Headache after injury"]
        }
        
        disease_lower = disease.lower()
        specific_guidelines = disease_specific.get(disease_lower, [])
        
        return {
            'general': general_guidelines,
            'disease_specific': specific_guidelines,
            'urgent': symptoms_severity == 'high'
        }

