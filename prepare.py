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
    
    # impute missing values for age based on mean for each sample
    import warnings
    warnings.filterwarnings("ignore")

    from sklearn.impute import SimpleImputer

    my_strategy = 'mean'
    column_list = ['age']

    def impute(train, validate, test, my_strategy, column_list):
        imputer = SimpleImputer(strategy=my_strategy)
        train[column_list] = imputer.fit_transform(train[column_list])
        validate[column_list] = imputer.transform(validate[column_list])
        test[column_list] = imputer.transform(test[column_list])
        return train, validate, test
    return test, train, validate