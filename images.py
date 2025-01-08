import os
import re
import shutil

# Paths
posts_dir = "/Users/ydderf/Workspace/projects/ydderfsblog/content/posts/"
attachments_dir = "/Users/ydderf/Vaults/C/2 - Source Material/Resources/"
static_images_dir = "/Users/ydderf/Workspace/projects/ydderfsblog/static/images/"

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"[*] Processing: {filepath}")
        
        with open(filepath, "r") as file:
            content = file.read()
        
        # Step 2: Find all image links in the format ![Image Description](/images/Pasted%20image%20...%20.png)
        images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
        
        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            # Prepare the Markdown-compatible link with %20 replacing spaces
            image_link = f"/images/{image.replace(' ', '%20')}"
            markdown_image = f"![Image Description]({image_link})"
            content = content.replace(f"![[{image}]]", markdown_image)
            
            # Step 4: Copy the image to the Hugo static/images directory if it exists
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                shutil.copy(image_source, static_images_dir)

        end_of_tag = content.find("---", 3) + 4
        start_of_title = content.find("#", end_of_tag)
        content = content[:end_of_tag] + content[start_of_title:]

        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w") as file:
            file.write(content)

print("[*] Done")
