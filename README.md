Live Demo:
https://predictive-maintenance-mlops-akmzvpb7bgmju6zn9bbfqu.streamlit.app/


#  Real-Time Industrial Predictive Maintenance Platform

An end-to-end MLOps predictive maintenance architecture designed to ingest real-time factory machinery sensor streams, dynamically fuse asset metadata profiles, and evaluate instant breakdown risks using machine learning models.

##  Key Engineering Pillars

* **Automated Feature Processing:** Implements a dynamic transformation layer to compute live mechanical variables (like rotational power in Watts, thermal core deltas, and multi-variable tool overstrain factors) while isolating dynamic data states to prevent leakage.
* **Persistent SQL Storage Fusing:** Integrates an optimized database layer utilizing local SQLite binary engines to run sub-millisecond parameterized metadata lookups, matching live machine IDs with their quality specification profiles on the fly.
* **Production-Grade API Gateway:** Implements structural data routing endpoints using FastAPI wrapped in strict Pydantic (`Annotated` and `Field`) typing schemas to completely shield the underlying ML inference layer from corrupted payloads.
* **Responsive Control Room UI:** Features a highly responsive executive web interface dashboard built using Streamlit, transitioning telemetry streams away from raw JSON formats into intuitive visual alert indicators.

---

## 📊 Core System Communication Architecture

The system decouples the front-end user experience from the analytical back-end engine. Telemetry states captured by input elements are serialized into validated network JSON payloads and piped across thread-safe HTTP channels to the model worker node:

```text
  ┌──────────────────────────────────────────────────────────┐
  │                 STREAMLIT EXECUTIVE UI                   │
  │     (Accepts Numeric Sensor Parameters on Port 8501)     │
  └────────────────────────────┬─────────────────────────────┘
                               │
                               │  [HTTP POST JSON Payload]
                               ▼
  ┌──────────────────────────────────────────────────────────┐
  │                   FASTAPI API GATEWAY                    │
  │     (Runs Data Validation Protocols on Port 8000)        │
  └────────────────────────────┬─────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌────────────────────────┐            ┌────────────────────────┐
│   SQLITE ASSET DB      │            │  SCIKIT-LEARN MODEL    │
│ (Sub-ms Profile Sync)  │            │ (Live Probability Run) │
└────────────────────────┘            └────────────────────────┘
