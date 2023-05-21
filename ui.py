import streamlit as st
from src import innoscripta

def search(company_name: str, company_country: str, company_website: str = None):
    """
    Build Innoscripta searcher
    """
    searcher = innoscripta.Innoscripta(name=company_name, country=company_country, website=company_website)
    info = searcher.main()
    return info

def show_images(urls_to_images: list):
    # Default text to display if an image is missing
    default_text = 'No image available'

    # Make sure the list always has 5 items
    while len(urls_to_images) < 5:
        urls_to_images.append(default_text)

    # Display all items in a grid
    col1, col2 = st.columns(2)

    for i in range(2):
        col1.image(urls_to_images[i] if urls_to_images[i] != default_text else default_text, use_column_width=True)
        col2.image(urls_to_images[i+2] if urls_to_images[i+2] != default_text else default_text, use_column_width=True)

    # Display the last item centered in the middle
    if urls_to_images[-1] != default_text:
        st.image(urls_to_images[-1], use_column_width=True)
    else:
        st.write(default_text)

def print_text(my_list):
    for item in my_list:
        with st.container():
            st.text(item)

def main():
    st.title('Company Information')

    company_name = st.text_input('Company Name', placeholder='Innoscripta')
    company_country = st.text_input('Company Country', placeholder='Germany')
    company_website = st.text_input('Company URL', placeholder='https://www.innoscripta.com/')

    # Display outputs
    if st.button('Submit'):

        with st.spinner("Please wait..."):
            info = search(company_name, company_country, company_website)
        
        st.header(f"Products and Services of {company_name}")
        print_text(info['products_services'])
        #st.write(f"Products/Services: {info['products_services']}")
        st.header(f"Keywords of {company_name}")
        print_text(info['keywords'])
        #st.write(f"Keywords: {info['keywords']}")
        st.header(f"Company Classification of {company_name}")
        print_text(info['company_classification'])
        #st.write(f"Classification: {info['company_classification']}")
        st.header(f"Additional informations of {company_name}")
        st.write(info['additional_informations'])
        #st.write(f"Additional Information: {info['additional_informations']}")

        show_images(info['images'])

if __name__ == "__main__":
    main()