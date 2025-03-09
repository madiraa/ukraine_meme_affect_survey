library(dplyr)
library(readr)
library(ggplot2)
library(tidyr)

rm(list = ls())


setwd("C:/Users/miavelli/Desktop/programs/ukraine_meme_affect_survey/ukraine_aid_survey_analytics")

df <- read_csv("raw.csv")

##################################
##################################
# Transform data into properly coded variables for regressions and subgrouping # 
##################################
##################################

# filter data 
df <- select(df, c("Q1", "Q2", "Q3", "Q21", "Q22", "Q23", "Q24", "Q4", "Q5_1","Q5_2","Q5_3","Q5_4","Q5_5","Q5_6","Q6","Q7","Q8","Q9","Q10","Q11","Q12","Q13","Q14","Q15"))
# Replace NA values with 0 for all columns #THIS SEEMS BAD 
df <- df %>%
  mutate_all(~ replace(., is.na(.), 0))
# Convert "I read the snippet" to 1 and NA to 0 for columns Q21, Q22, and Q23
df <- df %>%
  mutate_at(vars(Q21:Q23), ~ ifelse(. == "I read the snippet", 1, 0))
# Convert "ok" to 1 and NA to 0 for column Q24
df <- df %>%
  mutate(Q24 = ifelse(Q24 == "ok", 1, ifelse(is.na(Q24), 0, Q24)))
# rename columns to reflect treatments
df <- df %>%
  rename(adversary_message = Q21,
         aid_fact = Q22,
         ukr_need = Q23,
         control = Q24)

# transform support/oppose into binary variables 
columns_to_transform <- c("Q5_1", "Q5_2", "Q5_3", "Q5_4", "Q5_5", "Q5_6")
df <- df %>%
  mutate_at(vars(columns_to_transform), ~ ifelse(. == "Support", 1, ifelse(. == "Oppose", 0, .)))

# mutate Q4 column into 3 column with binary variable
df <- mutate(df,
             too_much = as.integer(Q4 == "Too much"),
             too_little = as.integer(Q4 == "Too little"),
             about_right = as.integer(Q4 == "About the right amount"))

# Partisanship 7 point scale transformation 
# Define a function to map the responses to the corresponding codes
map_to_code <- function(Q6, Q7, Q8, Q9) {
  if (Q7 == "Strong Democrat") {
    return(0)
  } else if (Q7 == "Not very strong Democrat") {
    return(1)
  } else if (Q6 == "Independent" || Q6 == "Something else") {
    if (Q9 == "Democratic party") {
      return(2)
    } else if (Q9 == "Neither") {
      return(3)
    } else if (Q9 == "Republican party") {
      return(4)
    }
  } else if (Q8 == "Not very strong Republican") {
    return(5)
  } else if (Q8 == "Strong Republican") {
    return(6)
  }
}
# Apply the function to create a new variable representing the 7-point scale
df$partisan_score <- mapply(map_to_code, df$Q6, df$Q7, df$Q8, df$Q9)

# Transform all partisan scores into binary
df <- mutate(df,
             strong_dem = ifelse(partisan_score == "0", 1, 0),
             not_strong_dem = ifelse(partisan_score == "1", 1, 0),
             ind_close_dem = ifelse(partisan_score == "2", 1, 0), 
             ind = ifelse(partisan_score == "3", 1, 0), 
             ind_close_rep = ifelse(partisan_score == "4", 1, 0), 
             not_strong_rep = ifelse(partisan_score == "5", 1, 0), 
             strong_rep = ifelse(partisan_score == "6", 1, 0), 
)

# transform various aid type binary responses 
df = df %>%
  rename("additional_arms" = Q5_1,
         "additional_econ" = Q5_2,
         "send_troops" = Q5_3,
         "sanction_rus" = Q5_4,
         "grad_decrease_mil_aid" = Q5_5,
         "grad_decrease_econ_aid" = Q5_6)            

# transform gender variable
df = mutate(df,
            is_man = ifelse(Q12 == "Man", 1, 0))

# transform citizenship variable
df = mutate(df, 
            is_citizen = ifelse(Q15 == "Yes",1,0))

# transform advantage 
df = mutate(df, 
            rus_advantage = ifelse(Q1 == "Russia has the advantage",1,0),
            ukr_advantage = ifelse(Q1 == "Ukraine has the advantage",1,0),
            neither_advantage = ifelse(Q1 == "Neither side has the advantage",1,0)
)