from django import template

register = template.Library()

@register.filter(name='indian_rupee')
def indian_rupee(value):
    """
    Formats a number into the Indian numbering system (e.g., 1,00,00,000.00).
    """
    try:
        if value is None:
            return ""
        
        # Convert to string to safely split decimal parts
        str_val = str(value)
        dec_str = ""
        
        # Separate integer and decimal parts
        if '.' in str_val:
            int_part, dec_part = str_val.split('.')
            # Only keep up to 2 decimal places, or don't display if it's .00
            if dec_part != '00' and float(f"0.{dec_part}") > 0:
                dec_str = f".{dec_part[:2]}"
        else:
            int_part = str_val

        # Handle formatting logic
        is_negative = int_part.startswith('-')
        if is_negative:
            int_part = int_part[1:]

        if len(int_part) > 3:
            last_3 = int_part[-3:]
            other = int_part[:-3]
            
            # insert comma every two digits from the right
            other_with_commas = ""
            while len(other) > 0:
                if len(other) > 2:
                    other_with_commas = "," + other[-2:] + other_with_commas
                    other = other[:-2]
                else:
                    other_with_commas = other + other_with_commas
                    other = ""
                    
            formatted = other_with_commas + "," + last_3
        else:
            formatted = int_part

        result = formatted + dec_str
        return f"-{result}" if is_negative else result
        
    except Exception:
        return value
