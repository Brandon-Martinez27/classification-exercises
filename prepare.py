#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def prep_iris(df):
    # a. Use the function defined in acquire.py to load the iris data.
    import acquire as a
    iris = a.get_iris_data()
    
    # b. Drop the species_id and measurement_id columns.
    iris.drop(['species_id'], axis=1, inplace=True)
    
    # c. Rename the species_name column to just species.
    iris.rename(columns={'species_name':'species'}, inplace=True)
    
    # d. Create dummy variables of the species name.
    iris_dummies = pd.get_dummies(iris[['species']], drop_first=False)
    new_iris = pd.concat([iris, iris_dummies], axis=1)
    
    return new_iris


# In[ ]:


def prep_titanic(df):
    # load the titanic data set.
    titanic = a.get_titanic_data()
    
    # Handle the missing values in the embark_town and `embarked' columns.
    titanic = titanic[titanic.embark_town.notnull()]
    
    # Remove the deck column.
    titanic.drop(columns='deck', inplace=True)
    
    # Create a dummy variable of the embarked column.
    titanic_dummies = pd.get_dummies(titanic['embarked'])
    titanic = pd.concat([titanic, titanic_dummies], axis=1)
    
     #Fill the missing values in age. Use train test validate samples to fill each with mean age of each sample
    from sklearn.model_selection import train_test_split

    train_validate, test = train_test_split(titanic, test_size=.2,
                                       random_state=123,
                                       stratify=titanic.survived)
    train, validate = train_test_split(train_validate, test_size=.3, 
                                   random_state=123, 
                                   stratify=train_validate.survived)
    test.fillna(value=test.age.mean(), inplace=True)
    train.fillna(value=train.age.mean(), inplace=True)
    validate.fillna(value=validate.age.mean(), inplace=True)
    return test, train, validate

