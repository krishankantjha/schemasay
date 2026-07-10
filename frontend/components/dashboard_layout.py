"""
SchemaSay Components — Dashboard Grid Layout Skeleton

Generates the structured wireframe card nodes for Phase 4.
All cards are created empty, serving as layout slots for subsequent phases.
"""

def render_dashboard_layout() -> str:
    """
    Renders the responsive wireframe layout consisting of three rows of empty cards:
      - Row 1: Left Card, Right Card
      - Row 2: Left Card, Center Card (Noticeably wider), Right Card
      - Row 3: Full Width Card
    """
    grid_html = """
    <div class="dashboard-container">
        <!-- Row 1: AI Copilot & SQL Workbench slots -->
        <div class="dashboard-row">
            <div class="col-row1-left">
                <div class="dashboard-card card-r1-left"></div>
            </div>
            <div class="col-row1-right">
                <div class="dashboard-card card-r1-right"></div>
            </div>
        </div>

        <!-- Row 2: Schema Explorer, Results panel, Query History slots -->
        <div class="dashboard-row">
            <div class="col-row2-left">
                <div class="dashboard-card card-r2-left"></div>
            </div>
            <div class="col-row2-center">
                <div class="dashboard-card card-r2-center"></div>
            </div>
            <div class="col-row2-right">
                <div class="dashboard-card card-r2-right"></div>
            </div>
        </div>

        <!-- Row 3: Full width card slot -->
        <div class="dashboard-row">
            <div class="col-row3-full">
                <div class="dashboard-card card-r3-full"></div>
            </div>
        </div>
    </div>
    """
    
    return grid_html
