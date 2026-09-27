import seaborn as sns
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

if not os.path.exists('titanic.csv'):  # checking for titanic.csv file exists in current directory if its not there load from sns and save using to_csv
    print(" file not there")
    titanic=sns.load_dataset("titanic")
    titanic.to_csv("titanic.csv",index=False)
else:           
    titanic=pd.read_csv("titanic.csv") # reading file from current directory 

    titanic.info()
    print(titanic.describe())
    # checking for how many rows and columns
    print(titanic.shape)

    # checking of string columns for mismatch of capitlas,small,title, case sensitive etc
    print(titanic["sex"].unique())
    print(titanic["embarked"].unique())
    # we found embarked column has nan records
    print(titanic["class"].unique())
    print(titanic["who"].unique())
    print(titanic["deck"].unique())
    print(titanic["embark_town"].unique())
    # we found embark_town has nan 
    print(titanic["alive"].unique())

    # checking for null total ,percentage column wise
    print(titanic.isnull().sum())
    print(titanic.isnull().mean()*100)
    # age column is having null percentage 19.86 as per instruction we impute nan values with median
    # pclass is labeling of class so we can check columns are equal after labeling and delete
    # embarked,embarked_town one column can be removed as embarked is short nameing of embarked_town both have 0.2 percent nan values so we can remove this rows
    # columns alive if we apply label coding and check with survived column both are like
    titanic['alive_label']=titanic["alive"].map({"yes":1,"no":0})
    is_equal = titanic['survived'].equals(titanic["alive_label"])
    if is_equal==True:
        titanic.drop(columns=["alive","alive_label"],inplace=True)
    titanic["embark_town_label"]=titanic["embark_town"].map({"Southampton":"S","Cherbourg":"C","Queenstown":"Q"})
    is_equal=titanic["embarked"].equals(titanic["embark_town_label"])      
    if is_equal==True:
        titanic.drop(columns=["embark_town","embark_town_label"],inplace=True)     
    # deck column has 77 % missing values as per rules we can delete column
    titanic.drop(columns=["deck"],inplace=True)                                               
    titanic["class_label"]=titanic["class"].map({"Third":3,"Second":2,"First":1})
    is_equal=titanic["pclass"].equals(titanic["class_label"])
    if is_equal==True:
        titanic.drop(columns=["class_label","class"],inplace=True)  
    # we can remove embarked nan rows as its low than 5% as per rules
    titanic.dropna(subset=["embarked"],inplace=True)

    titanic["age"]=titanic["age"].fillna(titanic["age"].mean()) # filling nan values of age with median
    
    titanic.drop_duplicates(inplace=True) # checking how many duplicate records are there and droping those records
    titanic.info()
    titanic.to_csv("cleaned_titanic.csv")
   
    
    fare_stats=titanic["fare"].describe()
    #print(fare_stats)
    fareq1=fare_stats["25%"]
    fareq3=fare_stats["75%"]
    IQR=fareq3-fareq1
    out_upper=fareq3+(1.5*IQR)
    out_bottom=fareq1-(1.5*IQR)
    #print(out_bottom,out_upper)
    print(f" number of out liers in fare column {titanic[(titanic["fare"]>out_upper) | (titanic["fare"]<out_bottom)].shape[0]}")
    # there 90 outliers in fare column

    age_stats=titanic["age"].describe()
    #print(age_stats)
    ageq1=age_stats["25%"]
    ageq3=age_stats["75%"]
    IQR=ageq3-ageq1
    age_upper=ageq3+(1.5*IQR)
    age_bottom=ageq1-(1.5*IQR)
    print(f"number of outliers in age column {titanic[(titanic["age"]>age_upper) | (titanic["age"]<age_bottom)].shape[0]} ")
    # there are 26 outliers in age column

    fmean=titanic["fare"].mean()
    fmedian=titanic["fare"].median()
    fmode=titanic["fare"].mode()[0]

    amean=titanic["age"].mean()
    amedian=titanic["age"].median()
    amode=titanic["age"].mode()[0]

    print(f"stats of fare column mean {fmean}-- median {fmedian} -- mode {fmode} ")
    print(f"stats of fare columns show mean>median>mode its right skewed distribution")
    print(f"stats of age column mean {amean}-- median {amedian} -- mode {amode}")
    print(f" above age colum shows mean~mediam~mode shows data distribution is normal distribution")
    fig, axes = plt.subplots(5, 2, figsize=(14, 10))
    sns.set_theme(style="whitegrid")
    # Histogram
    sns.histplot(data=titanic, x="age",kde=True,  ax=axes[0, 0], color="skyblue")
    axes[0,0].axvline(amean, color="blue", linestyle="--", linewidth=2, label=f"Mean: {amean:.2f}")
    axes[0,0].axvline(amedian, color="green", linestyle="--", linewidth=2, label=f"Median: {amedian:.2f}")
    axes[0,0].axvline(amode, color="red", linestyle="--", linewidth=2, label=f"Mode: {amode:.2f}")
    axes[0,0].legend()
    axes[0, 0].set_title("Age Distribution (Histogram)")
    # Box Plot
    sns.boxplot(data=titanic, x="age", ax=axes[0, 1], color="lightgreen")
    axes[0, 1].set_title("Age Outliers (Box Plot)")

    # --- FARE PLOTS ---
    # Histogram
    sns.histplot(data=titanic, x="fare", kde=True,ax=axes[1, 0], color="salmon")
    axes[1, 0].axvline(fmean, color="blue", linestyle="--", linewidth=2, label=f"Mean: {fmean:.2f}")
    axes[1, 0].axvline(fmedian, color="green", linestyle="--", linewidth=2, label=f"Median: {fmedian:.2f}")
    axes[1, 0].axvline(fmode, color="red", linestyle="--", linewidth=2, label=f"Mode: {fmode:.2f}")
    axes[1, 0].legend()
    axes[1, 0].set_title("Fare Distribution (Histogram)")

    # Box Plot
    sns.boxplot(data=titanic, x="fare", ax=axes[1, 1], color="gold")
    axes[1, 1].set_title("Fare Outliers (Box Plot)")

    #plt.tight_layout()
    #plt.show()
    
   

   

    print(f"mean:{fmean}--median:{fmedian}--mode:{fmode}")
   
    fare_skew = titanic["fare"].skew()
    if fare_skew >= -0.5 and fare_skew <= 0.5:
        print(" column is Approxmately Symmetric(Balanced on both sides)")
    elif fare_skew > 0.5 and fare_skew < 1:
        print("column is Moderately Right Skewed( Positive skew)")
    elif fare_skew > 1:
        print("column is Highly Right Skewed( Heavy right tail)") 
    elif fare_skew < -1:
        print("column is Highly Left Skewed( Heavy left tail)")

    print(f"Fare Skewness Score: {fare_skew:.2f}")
    
    #understand what your scores mean, statistical standards classify skewness into these categories:
    #-0.5 to 0.5: Approximately Symmetric (Balanced on both sides)
    #0.5 to 1.0: Moderately Right-Skewed (Positive skew)
    #>1.0: Highly Right-Skewed (Heavy right tail)
    #(< -1.0): Highly Left-Skewed (Heavy left tail)


    print(titanic.groupby("sex")["survived"].value_counts())
    # out of 320 survived 214 are woman and 106 are man shows out of 788 320 survived means 458 not survived 27.5% women,13.62 men survived and 58.86% died out of 9.76% women 49.1% are male
    # shows women are having more survival rate then men
    print(titanic.groupby("pclass")["survived"].value_counts())
    # pclass shows  first class has high chances of living when compared to 2nd and 3rd and 3rd class has higher rate of not surviving
    print(titanic.groupby(["sex","pclass"])["survived"].value_counts())
    # sex and plcass show females related to 1st and 2nd classes have survived more than 95%, most of the males related to 3rd class have less survival rate
    
  
       

    # Strictly restrict to the 6 specified independent numeric columns
    target_numeric_cols = ["survived", "pclass", "age", "sibsp", "parch", "fare"]
    restricted_df = titanic[target_numeric_cols]

    # Calculate the Pearson correlation matrix
    corr_matrix = restricted_df.corr()

    # Render the 6x6 matrix as a Heatmap
    #plt.figure(figsize=(8, 6))
    #sns.set_theme(style="white")

    # Display numbers via annot, format to 2 decimals, and use an intuitive colormap
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f",ax=axes[2, 0], linewidths=0.5, vmin=-1, vmax=1)

    axes[2, 0].set_title("Restricted 6x6 Core Numeric Correlation Matrix", fontsize=14, pad=15)
    #plt.tight_layout()
    #plt.show()

    # Code snippet to programmatically extract and print top absolute correlations
    corr_pairs = corr_matrix.unstack()
    corr_pairs = corr_pairs[corr_pairs.index.get_level_values(0) != corr_pairs.index.get_level_values(1)]
    top_two = corr_pairs.abs().sort_values(ascending=False)

    seen = set()
    print("--- Mathematically Ranked Top 2 Off-Diagonal Pairs ---")
    rank = 1
    for idx, abs_val in top_two.items():
        pair = tuple(sorted(idx))
        if pair not in seen and rank <= 2:
            seen.add(pair)
            print(f"Rank {rank}: {idx} & {idx} -> Correlation: {corr_pairs[idx]:.4f}")
            rank += 1

    

    # Set chart size and layout style
    #plt.figure(figsize=(10, 6))
    #sns.set_theme(style="whitegrid")

    # Create the overlaid density histogram
    # stat="density" normalizes the bins; common_norm=False treats groups independently
    sns.histplot(
        data=titanic,
        x="age",
        hue="survived",
        stat="count",
        common_norm=False,
        element="step",
        palette="Set1",
        alpha=0.4,
        binwidth=5,
        ax=axes[2, 1]
    )

    # Structural labels and titles
    axes[2, 1].set_title("Normalized Passenger Age Count: Survivors vs. Non-Survivors", fontsize=14, pad=15)
    axes[2, 1].set_xlabel("Passenger Age (Years)", fontsize=11)
    axes[2, 1].set_ylabel("Passenger Count", fontsize=11)

    # Configure explicit legend matching the categorical colors
    axes[2, 1].legend(title="Survival Status", labels=["Survived (1)", "Died (0)"])

    #plt.tight_layout()
    #plt.show()
    
    #The Early Childhood Peak (Ages 0–8): Unlike standard frequency histograms, the normalized density curve for survivors (Survived = 1) spikes significantly higher than the non-survivor curve in the youngest age bracket. 
    #This mathematically proves that, relative to their population size, children had an exceptionally high probability of being rescued.
    #The Young Adult Disparity (Ages 20–35): There is a clear density crossover in the young adult range, where the non-survivor curve (Died = 0) dominates. 
    #This indicates that while young adults made up a large portion of the passengers, their proportional survival rate was drastically reduced—mostly driven by the evacuation protocol prioritizing women and children over adult working-class men.
    
  

    # Set up the chart layout and grid style
    #plt.figure(figsize=(10, 6))
    #sns.set_theme(style="whitegrid")

    # Create the overlaid density histogram
    # stat="density" evaluates structural probability; common_norm=False treats target subsets independently
    sns.histplot(
        data=titanic,
        x="fare",
        hue="survived",
        stat="count",
        common_norm=False,
        element="step",
        palette="Set2",
        alpha=0.4,
        binwidth=5,
        ax=axes[3,0]
    )

   
    #axes[3,0].set_xlim(0, 200)

    # Set descriptive titles and axes titles
    axes[3,0].set_title("Normalized Passenger Fare Count: Survivors vs. Non-Survivors", fontsize=14, pad=15)
    axes[3,0].set_xlabel("Passenger Fare (Ticket Price up to 200)", fontsize=11)
    axes[3,0].set_ylabel("Passenger Count", fontsize=11)

    # Configure the explicit categorical color legend
    axes[3,0].legend(title="Survival Status", labels=["Survived (1)", "Died (0)"])

    #plt.tight_layout()
    #plt.show()
    
    #The Low-Fare Fatality Peak (Fares Under 30): In the lower price tiers, the density profile for non-survivors (Died = 0) towers over the survivor curve. 
    #This statistically verifies that passengers holding economical 3rd-class tickets had a severely disproportionate likelihood of drowning, 
    #as they faced worse deck placement and evacuation delays.The High-Fare Survival Dominance (Fares Above 50):
    #  Once the ticket price passes the 50 threshold, the survivor density curve (Survived = 1) takes a permanent lead.
    #    This clear crossover point mathematically establishes that socioeconomic class and ticket investment directly controlled a passenger's chances of survival during the evacuation.
    
    

    #plt.figure(figsize=(8, 5))
    #sns.set_theme(style="whitegrid")

    # Sub-stratifying the categorical counts by survival outcome
    sns.countplot(data=titanic, x="sex", hue="survived", palette="Set1", ax=axes[3,1])

    axes[3,1].set_title("Passenger Count by Gender and Survival Status", fontsize=13, pad=12)
    axes[3,1].set_xlabel("Gender (Sex)", fontsize=11)
    axes[3,1].set_ylabel("Passenger Count", fontsize=11)
    axes[3,1].legend(title="Survival Status", labels=["Died (0)", "Survived (1)"])

    #plt.tight_layout()
    #plt.show()
    
    #Gender Disparity: The  plot shows that while the absolute volume of male passengers on the ship was much higher, the raw count of male fatalities drastically dwarfs female fatalities.
    
    #plt.figure(figsize=(8, 5))

    # Counting passenger distribution per ticket class
    sns.countplot(data=titanic, x="pclass", hue="survived", palette="Set2" ,ax=axes[4,0])

    axes[4,0].set_title("Passenger Count by Ticket Class and Survival Status", fontsize=13, pad=12)
    axes[4,0].set_xlabel("Passenger Class (Pclass)", fontsize=11)
    axes[4,0].set_ylabel("Passenger Count", fontsize=11)
    axes[4,0].legend(title="Survival Status", labels=["Died (0)", "Survived (1)"])

    #plt.tight_layout()
    #plt.show()
    
    #The  plot highlights that Class 3 had the largest concentration of passengers, but it also suffered a catastrophic volume of non-survivors compared to Classes 1 and 2 combined.
    
    #plt.figure(figsize=(8, 5))

    # Counting passenger frequencies based on boarding locations
    sns.countplot(data=titanic, x="embarked", hue="survived", palette="pastel" , ax=axes[4,1])

    axes[4,1].set_title("Passenger Count by Embarkation Port and Survival Status", fontsize=13, pad=12)
    axes[4,1].set_xlabel("Embarkation Port", fontsize=11)
    axes[4,1].set_ylabel("Passenger Count", fontsize=11)
    axes[4,1].legend(title="Survival Status", labels=["Died (0)", "Survived (1)"])

    

    
    #the plot highlights that Southampton has  the largest concentration of passengers, but it also suffered a catastrophic volume of non-survivors compared to others
    
    print(f"mean {titanic['age'].mean():.4f} ")
    print(f"mean {titanic['fare'].mean():.4f} ")
    print(f"std {titanic['age'].std():.4f} ")
    print(f"std {titanic['fare'].std():.4f} ")
    scaler = StandardScaler()
    scaled_matrix = scaler.fit_transform(titanic[["age", "fare"]])
    #print(scaled_matrix)
    print(f"mean {scaled_matrix[:, 0].mean():.4f}")
    print( f"mean {scaled_matrix[:, 1].mean():.4f}")
    print(f"std {scaled_matrix[:, 0].std():.4f}")
    print( f"std {scaled_matrix[:, 1].std():.4f}")
    
    plt.tight_layout()
    plt.show()


