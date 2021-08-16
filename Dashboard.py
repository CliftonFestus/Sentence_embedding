import streamlit as st
import pandas as pd
import spacy
from spacy.matcher import Matcher
import func
import seaborn as sns
from matplotlib.pyplot import figure

from PIL import Image

image1 = Image.open('equation.png')


table_ = {'Category': ['Condition', 'Generalization', 'Modality', 'Numeric Quantifier'],
          'Meaning': ['Action(s) to be performed are dependent on a variable or unclear trigger.', 'Action(s)/Information Types are vaguely abstracted with unclear conditions.', 'Vague likelihood of action(s) or ambiguous possibility of action or event.', 'Vague quantifier of action/information type.'],
          'Examples': ["""depending, necessary, appropriate,
inappropriate, as needed, as applicable,
otherwise reasonably, sometimes, from time
to time""", """generally, mostly, widely, general, commonly,
usually, normally, typically, largely, often,
primarily, among other things""", """may, might, can, could, would, likely, possible,
possibly""", """anyone, certain, everyone, numerous, some,
most, few, much, many, various, including but
not limited to """]}

tab = pd.DataFrame(table_)

nav = st.sidebar.selectbox(
    "Navigation:-", ["Overview", "Scraped Policies", "Tool"])

if nav == "Overview":

    st.header("***Overview***")

    st.markdown("""# **Ambiguity Scoring in Privacy Policies**""")
    st.subheader(
        "**Corpus:** 73 privacy policies taken from publicly available apps on the Google Play Store")

    st.subheader("Inspiration")
    st.markdown(""" We have used the methodology from the paper [Ambiguity in Privacy Policies and the Impact of Regulation](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2715164) to quantify the degree of ambiguity in the set of privacy policies gathered. The paradigm they present categorizes ambiguous terms into the **four categories: Condition, Generalization, Modality and Numeric Quanitifiers**. The same have been described with examples in the table below.
     """)
    st.table(tab.set_index('Category'))

    st.subheader("Methodology")
    st.markdown(" The process involved scraping the privacy policies, categorizing the different terms into their respective categories, finding their probablities and finally giving them a vagueness score.")

    st.subheader("The Scoring Model ")
    st.markdown("""Simply  counting  the  number  of  vague  terms  in  a  privacy  policy  will  not  provide  an 
    adequate  measure  of  ambiguity. The score is based on a statistical measure 
    that scales the overall vagueness of individual statements in each policy based on the 
    Bradley-Terry model for paired comparisons.   """)

    st.markdown("""The  coefficients  that  were  computed  by  this  method  serve  for  these  calculations  to 
    rank  the  vagueness  of  every  phrase  in  each  policy  containing  a  vague  term  or 
    combinations  of  vague  terms  associated  with  an  action-information  pairing  where 
    one of  the four identified  data practices (action) is applied  to a type of information 
    (information).  """)

    st.image(image1, caption='Equation')

if nav == "Tool":
    st.header("***Tool***")

    # Scoring model text: pg 14
    st.subheader(
        "This tool will Analyse your text and give an everage privacy score.")
    myfile_text = st.text_area("Copy the policy text and paste here. ")

    if len(myfile_text) > 0:
        matrix = func.make_df(myfile_text)
        if "may" in matrix:

            st.write(matrix["Category"])
            st.write("Average vagueness score = ", matrix['BT Coeff'].mean())
        else:
            st.write("No vague terms found.Try again please.")

elif nav == "Scraped Policies":
    st.header("***Scraped Policies***")

    st.write(
        """To see the data analysis of the corpus, choose ***plots***. To see the average vague score for scraped policies choose ***scoring***""")

    pol_analysis = st.selectbox("Choose:-", ["Plots", "Scoring"])

    if pol_analysis == "Plots":

        st.write("Ambiguity score for each of the category: ")
        analysis = pd.read_csv('coef_prob_plot.csv')
        analysis.columns = ['category', 'bt_coef', 'Probability']

        st.write(analysis)

        score = figure(figsize=(10, 6), dpi=80)
        ax = sns.barplot(x="category", y="bt_coef", data=analysis)
        st.pyplot(score)

        st.write("\n\n\n\n\n")

        st.write("Probability of the words in each category: ")
        prob = figure(figsize=(10, 6), dpi=80)
        ax = sns.barplot(x="category", y="Probability", data=analysis)
        st.pyplot(prob)

    if pol_analysis == "Scoring":
        st.subheader("Average Vague Score of all the Phrases:- ")
        policies_data = pd.read_csv("Policies.csv")
        Company = policies_data['File_name']
        rad_comp = st.multiselect("Select the Company.", Company)

        for i in range(0, len(Company)):
            for a in rad_comp:
                if a == Company[i]:
                    st.write(Company[i], ":  ",
                             policies_data.loc[i, "vague_score"])
