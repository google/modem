**Note:** This is not an officially supported Google product. It is a reference
implementation.

# MoDeM

MoDeM (Model Deployment for Marketing) is a **Google Cloud based ETL pipeline**
for advertisers, interested in **ML-based audience retargeting**. The pipeline
extracts user data from BigQuery, runs it through the desired machine learning
model **(BigQueryML, scikit-learn, XGBoost, Tensorflow, AutoML)**, transforms
the model predictions into an audience list, loading it into Google Analytics,
for **eventual activation in Google Ads, Display & Video 360 and Search Ads
360.**

With marketers using increasingly sophisticated approaches in digital
advertising, there has been an exponential increase in number of analysts, data
scientists, and statisticians within marketing departments. While their
mathematical modelling skills are second to none, the long-term success of ML
projects hinge on making the jump from analysis to action. Often, analyst teams
hack together a process, that can be extremely manual and error-prone with too
many parameters, decoupled workflow dependencies and security vulnerabilities.
In fact, an entire discipline called MLOps has emerged that focuses on
operationaling machine learning workflows.

MoDeM hopes to provide the **last-mile engineering infrastructure** that enables
analysts to **quickly productionize & activate their models** with the necessary
operational and security rigor.

## Prerequisites

1.  **Client Id correctly captured in GA**. If using Data Import - any model
    that is created using client id and the desire is to create remarketing
    audiences based off the output of the query you need to ensure that clientId
    is captured as a custom dimension in GA. The pipeline will point the
    clientId field to the custom dimension and not the clientId for data import.
    You also cannot use User-Id.

## Instructions

1.  **BigQueryML models** using Cloud Functions & Cloud Scheduler / Compute
    Engine - [here](https://github.com/google/modem/blob/master/bqml/README.md)
2.  **Python ML models** with Google AI Platform (scikit-learn, XGBoost &
    Tensorflow) using Compute Engine -
    [here](https://github.com/google/modem/blob/master/pythonML/README.md)
3.  **AutoML models** using Compute Engine and/or AI Pipelines<sup>*</sup>.

--------------------------------------------------------------------------------

<sup>*</sup>*On the roadmap.*
