import streamlit as st

# Enhanced CSS for timeline styling
st.markdown("""
<style>
    /* Container for the entire timeline */
    .timeline {
        position: relative;
        margin: 2rem 0;
        padding-left: 2rem;
        border-left: 4px solid #457b9d;
    }

    /* Each timeline item */
    .timeline-item {
        position: relative;
        margin-bottom: 2rem;
        padding: 1rem 1.5rem;
        background: #f1faee;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .timeline-item:hover {
        transform: translateX(10px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }

    /* The dot on the timeline */
    .timeline-dot {
        position: absolute;
        left: -12px;
        top: 1.5rem;
        width: 20px;
        height: 20px;
        background: #e63946;
        border: 4px solid #f1faee;
        border-radius: 50%;
        box-shadow: 0 0 8px rgba(230, 57, 70, 0.6);
        transition: background 0.3s ease;
    }
    .timeline-item:hover .timeline-dot {
        background: #d62828;
        box-shadow: 0 0 12px rgba(214, 40, 40, 0.8);
    }

    /* Headings inline with dot */
    .timeline-item h3 {
        display: inline;
        color: #1d3557;
        margin-bottom: 0.3rem;
        font-weight: 700;
    }

    /* Paragraph styling */
    .timeline-item p {
        margin-top: 0.2rem;
        margin-bottom: 0.6rem;
        color: #333;
        line-height: 1.4;
    }

    /* Impact metric badge */
    .impact-metric {
        display: inline-block;
        background: #a8dadc;
        color: #1d3557;
        font-weight: 700;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        user-select: none;
        transition: background 0.3s ease;
    }
    .timeline-item:hover .impact-metric {
        background: #7bc4c8;
    }

    /* Section titles */
    h2 {
        color: #1d3557;
        margin-top: 3rem;
        margin-bottom: 1rem;
        font-weight: 800;
        font-size: 1.8rem;
    }

    /* Root cause text */
    p > strong {
        color: #457b9d;
        font-weight: 700;
        font-size: 1.1rem;
    }

    /* Responsive tweaks */
    @media (max-width: 600px) {
        .timeline {
            padding-left: 1rem;
            border-left-width: 3px;
        }
        .timeline-dot {
            left: -10px;
            width: 16px;
            height: 16px;
            border-width: 3px;
            top: 1.3rem;
        }
        .timeline-item {
            padding: 1rem 1rem 1rem 2rem;
            margin-bottom: 1.5rem;
        }
        h2 {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Content with enhanced styling
content = """
<h2>🏭 Warehouse Process Improvement</h2>
<p><strong>Root Cause Addressed:</strong> Slow loading/unloading times at key warehouses</p>

<div class="timeline">
    <div class="timeline-item">
        <span class="timeline-dot"></span>
        <h3>1. Implement Warehouse Automation</h3>
        <p>Install automated loading systems in Warehouses 5 and 7 (the slowest performers)</p>
        <div class="impact-metric">Expected Improvement: 40% faster processing</div>
    </div>
    <div class="timeline-item">
        <span class="timeline-dot"></span>
        <h3>2. Process Standardization</h3>
        <p>Create standardized work procedures across all warehouses</p>
        <div class="impact-metric">Expected Improvement: 15% consistency gain</div>
    </div>
    <div class="timeline-item">
        <span class="timeline-dot"></span>
        <h3>3. Performance Monitoring</h3>
        <p>Real-time tracking of loading/unloading times with alerts for delays</p>
        <div class="impact-metric">Expected Improvement: 20% faster issue resolution</div>
    </div>
</div>

<h2>🕒 Dynamic Shift Scheduling</h2>
<p><strong>Root Cause Addressed:</strong> Poor alignment between shift capacity and delivery demand</p>

<div class="timeline">
    <div class="timeline-item">
        <span class="timeline-dot"></span>
        <h3>1. Demand-Based Scheduling</h3>
        <p>Use historical data to align shift staffing with delivery volume patterns</p>
        <div class="impact-metric">Expected Improvement: 25% reduction in idle time</div>
    </div>
    <div class="timeline-item">
        <span class="timeline-dot"></span>
        <h3>2. Cross-Training Program</h3>
        <p>Train warehouse staff to perform multiple roles for better resource allocation</p>
        <div class="impact-metric">Expected Improvement: 15% productivity increase</div>
    </div>
    <div class="timeline-item">
        <span class="timeline-dot"></span>
        <h3>3. Incentive Program</h3>
        <p>Performance-based bonuses for shifts that meet productivity targets</p>
        <div class="impact-metric">Expected Improvement: 10% output increase</div>
    </div>
</div>

<h2>🗺️ Regional Network Redesign</h2>
<p><strong>Root Cause Addressed:</strong> Poor performance in East region</p>

<div class="timeline">
    <div class="timeline-item">
        <span class="timeline-dot"></span>
        <h3>1. Route Optimization</h3>
        <p>Implement dynamic routing software accounting for traffic patterns in East region</p>
        <div class="impact-metric">Expected Improvement: 30% faster deliveries</div>
    </div>
    <div class="timeline-item">
        <span class="timeline-dot"></span>
        <h3>2. Satellite Warehouse</h3>
        <p>Open a smaller distribution hub in East region to reduce last-mile delivery times</p>
        <div class="impact-metric">Expected Improvement: 40% reduction in East region delays</div>
    </div>
    <div class="timeline-item">
        <span class="timeline-dot"></span>
        <h3>3. Partner Network</h3>
        <p>Establish partnerships with local logistics providers in challenging areas</p>
        <div class="impact-metric">Expected Improvement: 20% cost reduction</div>
    </div>
</div>
"""

st.markdown(content, unsafe_allow_html=True)

