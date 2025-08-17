<style>
/* GitHub-like Markdown heading styles */

h1 {
  padding-bottom: 0.1em;
  font-size: 2em;
  border-bottom: 1px solid #50555aff;
  font-weight: 700;
  line-height: 1.25;
}

h2 {
  padding-bottom: 0.1em;
  font-size: 1.5em;
  border-bottom: 1px solid #8f959bff;
  font-weight: 600;
  line-height: 1.25;
}

h3 {
  font-size: 1.25em;
  font-weight: 600;
}

h4 {
  font-size: 1em;
  font-weight: 600;
}

h5 {
  font-size: 0.875em;
  font-weight: 600;
}

h6 {
  font-size: 0.85em;
  color: #57606a;
}
</style>






<div style="text-align: center; font-size: 40px;font-weight: 800">
  Ingeniería de datos

  Práctica
</div>

comment for the copilot: this is a summary of the data engineering course from aws 

# The elements of data

## The 5 Vs of data

- Velocity: How frequently data is generated? 
- Variety: How many sources and formats?
- Veracity: How accurate and trusted is the data?
- Value: What insights can be pulled?
- Volume: How much data is generated?
  
**how to get value?**
- confirm the need can be met
- evaluate if data can be acquired
- match design to data
- ROI (balance throughput and cost)
- Users focus on business
- Catalog and governance
  
## Volume and velocity

**Volume and velocity touch every part of the pipeline:**
- Ingestion: Scale pipelines to handle the volume at the pace of its arrival
- Storage: How long data should be stored
- Processing: How much data should be processed and how quickly to address a business problem
- Visualization: How much data users need and how frequently it should be updated

## Variety - Data types

- Structured: (SQL database)
    - well defined schema. Easy to query. Not flexible. Hot(ready to analyze)
- Semi-structured: (JSON, XML, Parquet, CSV)
    - Some schema. Easy to query. Flexible.
- Unstructured: (Text, images, audio, video)
    - No schema. Hard to query. Flexible.

##






