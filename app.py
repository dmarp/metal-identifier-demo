import streamlit as st
import cv2
import numpy as np

def classify_metal(image, weight, volume, color, spark, scratch, magnetic):
    """
    A simplified metal classification function based on:
      - Density: computed from weight and volume.
      - Color description.
      - Spark test: qualitative input.
      - Scratch test: a rating for hardness/resistance.
      - Magnetic property: boolean.
      
    This demo uses basic if-else logic.
    """
    # Compute density (g/cc)
    density = weight / volume if volume > 0 else 0
    
    # Initialize result
    result = "Unknown metal. Please check your inputs."
    
    # Decision logic:
    if magnetic:
        if density >= 7.0:
            result = "Likely Iron or Steel"
        else:
            result = "Possibly Magnetic Stainless Steel"
    else:
        # Using color hints and density
        if "red" in color.lower() or "copper" in color.lower():
            result = "Likely Copper"
        elif "gold" in color.lower() or "yellow" in color.lower():
            result = "Likely Brass or Bronze"
        elif density < 3.5:
            result = "Likely Aluminum"
        else:
            result = "Metal type uncertain. Further testing required."
    
    # Optionally, you might refine based on spark and scratch test results
    # (This is where advanced image/signal analysis logic would be integrated.)
    return result

def main():
    st.title("Metal Type and Alloy Identifier Demo")
    st.write("Upload an image and input test values to identify the metal type.")
    
    # Image upload section
    uploaded_image = st.file_uploader("Upload Metal Image", type=["jpg", "png", "jpeg"])
    if uploaded_image is not None:
        # Convert the uploaded file to a NumPy array for OpenCV
        file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        # Convert color from BGR (OpenCV) to RGB for display in Streamlit
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.image(image_rgb, caption="Uploaded Metal Image", use_column_width=True)
    else:
        st.info("No image uploaded. You can still input values for a demo classification.")
    
    st.header("Input Test Values")
    weight = st.number_input("Weight (grams)", min_value=0.0, value=100.0, step=0.1)
    volume = st.number_input("Volume (cubic centimeters)", min_value=0.1, value=10.0, step=0.1)
    color = st.text_input("Predominant Color (e.g., silver, red, yellow)", "silver")
    spark = st.selectbox("Spark Test Result", ["Long Sparks", "Short Sparks", "No Sparks"])
    scratch = st.slider("Scratch Test Rating (1 = soft, 10 = very hard)", 1, 10, 5)
    magnetic = st.checkbox("Is it Magnetic?")
    
    if st.button("Identify Metal"):
        result = classify_metal(None, weight, volume, color, spark, scratch, magnetic)
        st.success(f"Identification Result: {result}")
        st.info(f"Computed Density: {weight/volume:.2f} g/cc")
    
if __name__ == "__main__":
    main()
