# mixed-levelm logistic regression mediation using the 'lavaan' package
# Anne Urai, 2022

library("lavaan")
#library("lavaanPlot")
#library("semPlot")
set.seed(2021)

# load data
datapath <- '/Users/urai/Documents/code/ddm_mediation'
datapath <- '/home/uraiae/code/ddm_mediation' # on ALICE

for (eff_x in list('v', 'z', 'no')) { 
  for (eff_m in list('v', 'z', 'no')){

    mydata = read.csv(sprintf("%s/data/data_df_X%s_M%s.csv", datapath, eff_x, eff_m))
    
    # make sure response is a logical array, so logistic regression is used!
    mydata$response <- factor(mydata$response)
    mydata$S <- factor(mydata$S)
    
    # ============================= #
    
    singleMediation <- '
                          # first, define the regression equations
                          M ~ a * X
                          response ~ b * M + c * X + s0 * S
    
                          # define the effects
                          indirect := a * b
                          direct    := c
                          total     := c + (a * b)
                          '
    
    # ============================= #
    # loop over subjects
    mediation_results  <- data.frame()
    
    for ( subj in unique(c(mydata$subj_idx)) ) {
      tmpdata <- mydata[(mydata$subj_idx == subj),]
      fit <- sem(model = singleMediation, 
                 data = tmpdata, 
                 ordered=c("response"),
                 estimator='WLSMV')
      param_estimates <- parameterEstimates(fit, standardized = TRUE)
    
      # append to dataframe
      summ2 = as.data.frame(param_estimates)
      summ2$subj_idx <- subj
      mediation_results <- rbind(mediation_results, summ2) # append
      write.csv(mediation_results, sprintf("%s/data/fit_lavaan_X%s_M%s.csv", datapath, eff_x, eff_m)) # write at each iteration
      print(sprintf("%s/data/fit_lavaan_X%s_M%s.csv", datapath, eff_x, eff_m))
    }
  }
}