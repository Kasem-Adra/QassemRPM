import re
import os

def validate_spec(spec_path):
    if not os.path.exists(spec_path):
        return False, f"File not found: {spec_path}"
    
    # الوسوم الإلزامية المطلوبة في Issue #8
    mandatory_tags = ['Name', 'Version', 'Release', 'Summary', 'License', 'URL']
    found_tags = {}
    
    try:
        with open(spec_path, 'r') as f:
            content = f.read()
            for tag in mandatory_tags:
                # البحث عن الوسم في بداية السطر متبوعاً بنقطتين
                match = re.search(rf'^{tag}:\s*(.*)', content, re.MULTILINE)
                if match:
                    found_tags[tag] = match.group(1).strip()
                else:
                    found_tags[tag] = None

        missing = [t for t, v in found_tags.items() if v is None]
        
        if missing:
            return False, f"Missing mandatory tags: {', '.join(missing)}"
        
        return True, "SPEC file is valid."
    except Exception as e:
        return False, f"Error reading file: {str(e)}"
