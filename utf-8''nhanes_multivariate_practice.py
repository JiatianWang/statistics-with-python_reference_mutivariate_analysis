
# coding: utf-8

# # Practice notebook for multivariate analysis using NHANES data
# 
# This notebook will give you the opportunity to perform some multivariate analyses on your own using the NHANES study data.  These analyses are similar to what was done in the week 3 NHANES case study notebook.
# 
# You can enter your code into the cells that say "enter your code here", and you can type responses to the questions into the cells that say "Type Markdown and Latex".
# 
# Note that most of the code that you will need to write below is very similar to code that appears in the case study notebook.  You will need to edit code from that notebook in small ways to adapt it to the prompts below.
# 
# To get started, we will use the same module imports and read the data in the same way as we did in the case study:

# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels.api as sm
import numpy as np

da = pd.read_csv("nhanes_2015_2016.csv")
da.columns


# ## Question 1
# 
# Make a scatterplot showing the relationship between the first and second measurements of diastolic blood pressure ([BPXDI1](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/BPX_I.htm#BPXDI1) and [BPXDI2](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/BPX_I.htm#BPXDI2)).  Also obtain the 4x4 matrix of correlation coefficients among the first two systolic and the first two diastolic blood pressure measures.

# In[14]:



print(da.loc[:,['BPXSY1','BPXSY2','BPXDI1','BPXDI2']].corr())


plt.figure(figsize = (10,10))
plt.subplot(2,2,1)
sns.regplot(x = 'BPXDI1', y = 'BPXDI2', data = da, fit_reg = False, scatter_kws = ({'alpha' : 0.2}))
plt.subplot(2,2,2)
sns.regplot(x = 'BPXDI1', y= 'BPXSY1', data = da,fit_reg = False, scatter_kws = ({'alpha' : 0.2}))
plt.subplot(2,2,3)
sns.regplot(x = 'BPXDI1', y= 'BPXSY2', data = da,fit_reg = False, scatter_kws = ({'alpha' : 0.2}))
plt.subplot(2,2,4)
sns.regplot(x = 'BPXDI2', y= 'BPXSY2', data = da,fit_reg = False, scatter_kws = ({'alpha' : 0.2}))


# __Q1a.__ How does the correlation between repeated measurements of diastolic blood pressure relate to the correlation between repeated measurements of systolic blood pressure?

# __Q2a.__ Are the second systolic and second diastolic blood pressure measure more correlated or less correlated than the first systolic and first diastolic blood pressure measure?

# ## Question 2
# 
# Construct a grid of scatterplots between the first systolic and the first diastolic blood pressure measurement.  Stratify the plots by gender (rows) and by race/ethnicity groups (columns).

# In[3]:


da["RIAGENDRx"] = da.RIAGENDR.replace({1: "Male", 2: "Female"})
_ = sns.FacetGrid(da, col ='RIDRETH1' , row = "RIAGENDRx").map(plt.scatter,'BPXDI1','BPXSY1',alpha = 0.5)


# __Q3a.__ Comment on the extent to which these two blood pressure variables are correlated to different degrees in different demographic subgroups.

# we are look to stratifyigng the data by gender and ethnicity. This results in 2 x 5 = 10 total strata, sicne ther are 2 gender strata and 5 ethnicity strata. These scatterplots reveal difference in the means as well a differences in the degree of association(correlation) between differenct pairs of variables. we see that although some ethnic group tend to have highw blood pressure, the relationship between first systolic and first diastolic blood pressure is roughly similar across the group.

# ## Question 3
# 
# Use "violin plots" to compare the distributions of ages within groups defined by gender and educational attainment.

# In[23]:


da["DMDEDUC2x"] = da.DMDEDUC2.replace({1: "<9", 2: "9-11", 3: "HS/GED", 4: "Some college/AA", 5: "College", 
                                       7: "Refused", 9: "Don't know"})
da["RIAGENDRx"] = da.RIAGENDR.replace({1: "Male", 2: "Female"})


dx = da.loc[(da["DMDEDUC2x"] != "Don't know") & (da["DMDEDUC2x"] != "Refused")]
plt.figure(figsize = (12,4))
sns.violinplot(dx.DMDEDUC2x, da.RIDAGEYR, hue =dx.RIAGENDRx)


# __Q4a.__ Comment on any evident differences among the age distributions in the different demographic groups.

# We can see quite clearly that distributions(HS/GED, 9-11) with interdediate mean are approximately sysmmertraically distributed with bimomal shape
# The distribution with low mean(college) is right-skewed, and distribution(<9) has the oppotite trend.  

# ## Question 4
# 
# Use violin plots to compare the distributions of BMI within a series of 10-year age bands.  Also stratify these plots by gender.

# In[6]:


da["RIDAGEYRx"] = pd.cut(da["RIDAGEYR"], [20,30,40,50,60,70,80])
plt.figure(figsize = (12,4))
sns.violinplot(da.RIDAGEYRx, da.BMXBMI,hue= da.RIAGENDRx)


# __Q5a.__ Comment on the trends in BMI across the demographic groups.

# All the distributions with all range of age band are strongly right-skewed.

# ## Question 5
# 
# Construct a frequency table for the joint distribution of ethnicity groups ([RIDRETH1](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.htm#RIDRETH1)) and health-insurance status ([HIQ210](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/HIQ_I.htm#HIQ210)).  Normalize the results so that the values within each ethnic group are proportions that sum to 1.

# In[12]:


ft = pd.crosstab(da.RIDRETH1,da.HIQ210).apply(lambda x: x / x.sum(), axis = 1)
ftt = pd.crosstab(da.RIDRETH1,da.HIQ210,normalize= 'index')

print(ft)
print(ftt)


# __Q6a.__ Which ethnic group has the highest rate of being uninsured in the past year?
