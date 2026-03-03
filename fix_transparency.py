from PIL import Image
import glob

def fix_magenta(filepath):
    try:
        img = Image.open(filepath).convert("RGBA")
        data = img.getdata()
        
        # Determine background color by top-left pixel
        bg = data[0]
        
        new_data = []
        for item in data:
            # Check Euclidean distance to background color (allows threshold for anti-aliasing)
            dist = sum((a - b)**2 for a, b in zip(item[:3], bg[:3]))**0.5
            if dist < 65: # Threshold to capture any artifact magenta/pink
                new_data.append((255, 255, 255, 0)) # Fully transparent
            else:
                new_data.append(item)
                
        img.putdata(new_data)
        img.save(filepath, "PNG")
        print(f"Fixed {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

for f in ["assets/player.png", "assets/enemy.png", "assets/coin.png"]:
    fix_magenta(f)
