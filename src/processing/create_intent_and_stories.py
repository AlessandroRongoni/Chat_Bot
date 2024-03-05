import csv
from collections import defaultdict

input_file = '././dataset/Ubuntu-dialogue-corpus/dialogueText.csv'  # Sostituire con il percorso effettivo del tuo file CSV

# Strutture per memorizzare i dati estratti
intents_examples = defaultdict(list)
stories = []

def identify_intent(text):
    text = text.lower()
    if "java" in text:
        return "java_issues"
    elif "firefox" in text or "browser" in text:
        return "browser_issues"
    elif "ubuntu" in text:
        if "install" in text:
            return "ubuntu_installation"
        elif "version" in text or "release" in text:
            return "ubuntu_version_info"
        elif "dual boot" in text:
            return "ubuntu_dual_boot"
        elif "upgrade" in text or "update" in text:
            return "ubuntu_update"
    elif "vlc" in text:
        return "vlc_issues"
    elif "wireless" in text or "wifi" in text:
        return "wifi_issues"
    elif "bios" in text:
        return "bios_configuration"
    elif "samba" in text:
        return "samba_configuration"
    elif "nvidia" in text or "driver" in text:
        return "driver_issues"
    elif "xorg.conf" in text or "xorg" in text:
        return "xorg_configuration"
    elif "cd" in text or "dvd" in text:
        return "cd_dvd_issues"
    elif "password" in text or "login" in text:
        return "login_issues"
    elif any(word in text for word in ["error", "fail", "cannot", "can't", "problem"]):
        return "general_error"
    elif "hidden files" in text:
        return "hidden_files"
    elif "graphics card" in text or "onboard graphics" in text:
        return "graphics_card"
    elif "kernel" in text:
        if "log" in text:
            return "kernel_log_issues"
        elif "smp" in text:
            return "kernel_smp_switch"
    elif "dependencies" in text:
        return "dependencies_issues"
    elif "apt-get" in text:
        return "apt_get_usage"
    elif "kubuntu" in text:
        return "switch_to_kubuntu"
    elif "usb" in text:
        return "usb_issues"
    elif "virtualbox" in text:
        return "virtualbox_usage"
    elif "compiz" in text:
        return "compiz_issues"
    elif "flash" in text:
        return "flash_issues"
    elif "pidgin" in text:
        return "pidgin_connection"
    elif "kinect" in text:
        return "kinect_linux_driver"
    elif "transparency" in text or "effects" in text:
        return "ui_effects_issues"
    else:
        return "miscellaneous"


# Leggi il file CSV e estrai intenti e storie
with open(input_file, 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    dialogue_id = None
    for row in reader:
        # Identifica l'intento
        intent = identify_intent(row['text'])
        intents_examples[intent].append(row['text'])
        
        # Crea una storia per ogni dialogo unico (semplice esempio)
        if dialogue_id != row['dialogueID']:
            if dialogue_id is not None:
                stories.append(current_story)
            dialogue_id = row['dialogueID']
            current_story = {'name': f"dialogo_{dialogue_id}", 'steps': []}
        current_story['steps'].append({'intent': intent, 'action': f"azione_{intent}"})

    # Aggiungi l'ultima storia se non vuota
    if dialogue_id is not None and current_story not in stories:
        stories.append(current_story)

# Scrivi gli intenti in nlu.yml
with open('nlu.yml', 'w', encoding='utf-8') as nlu_file:
    nlu_file.write('version: "3.0"\n')
    nlu_file.write('nlu:\n')
    for intent, examples in intents_examples.items():
        nlu_file.write(f'- intent: {intent}\n  examples: |\n')
        for example in examples:
            nlu_file.write(f"    - {example}\n")

# Scrivi le storie in stories.yml
with open('stories.yml', 'w', encoding='utf-8') as stories_file:
    stories_file.write('version: "3.0"\n')
    stories_file.write('stories:\n')
    for story in stories:
        stories_file.write(f"- story: {story['name']}\n  steps:\n")
        for step in story['steps']:
            stories_file.write(f"  - intent: {step['intent']}\n    action: {step['action']}\n")
