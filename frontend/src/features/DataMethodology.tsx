export function DataMethodology() {
  return (
    <main
      id="data-methodology"
      className="main-content information-page"
    >
      <header className="information-hero">
        <p className="eyebrow">How ClimateCapital works</p>
        <h1>Data &amp; Methodology</h1>

        <p className="information-lead">
          <strong>
            ClimateCapital AI helps users explore Austin&apos;s 2026 bond
            projects and understand how different project budgets could shape
            a Funding Plan.
          </strong>
        </p>

        <p>
          The application uses City project information available as of{' '}
          <strong>January 21, 2026</strong>. This lets us examine the decision
          at that point in time without allowing information released later to
          influence the analysis.
        </p>

        <p>
          ClimateCapital uses transparent rules based on the City&apos;s
          project scores and funding requests to build Funding Plans. Gemini
          helps explain the projects, scores, and results in plain language,
          but it does not choose projects or change the calculations.
        </p>

        <aside className="information-callout">
          <strong>Historical decision-support simulation</strong>
          <span>
            ClimateCapital AI is a decision-support and historical simulation
            tool. It is not an official City of Austin recommendation.
          </span>
        </aside>
      </header>

      <div className="information-sections">
        <section aria-labelledby="snapshot-heading">
          <p className="eyebrow">Historical snapshot</p>
          <h2 id="snapshot-heading">Why January 21, 2026?</h2>

          <p>
            Think of January 21, 2026 as a <strong>snapshot in time</strong>.
          </p>

          <p>
            On that date, the City of Austin released its Initial Draft
            Recommendation for the 2026 Bond Program.
          </p>

          <p>
            ClimateCapital uses the project information available at that
            point so recommendations and outcomes that came later cannot
            influence the analysis.
          </p>

          <p>
            We call this the <strong>Historical Decision Snapshot</strong>.
          </p>
        </section>

        <section aria-labelledby="universe-heading">
          <p className="eyebrow">Project universe</p>
          <h2 id="universe-heading">Which projects are included?</h2>

          <p>
            Austin&apos;s <strong>Project Review Board (PRB)</strong> reviewed
            and scored proposed bond projects and programs.
          </p>

          <p>
            <strong>PRB stands for Project Review Board.</strong> It used a
            common scoring framework to help evaluate and prioritize requests
            for the 2026 Bond Program.
          </p>

          <p>
            ClimateCapital starts with <strong>136 PRB source rows</strong>{' '}
            and identifies <strong>106 individual projects</strong> that can
            be evaluated consistently at the project level.
          </p>

          <dl
            className="information-stat-grid"
            aria-label="Projects by category"
          >
            <div>
              <dt>Transportation</dt>
              <dd>9</dd>
            </div>
            <div>
              <dt>Parks &amp; Open Space</dt>
              <dd>22</dd>
            </div>
            <div>
              <dt>Watershed</dt>
              <dd>37</dd>
            </div>
            <div>
              <dt>Community Facilities</dt>
              <dd>38</dd>
            </div>
          </dl>

          <h3>Why aren&apos;t all 136 PRB rows shown as projects?</h3>

          <p>
            Some PRB rows represent broader programs or funding allocations
            rather than individual projects, and three items were explicitly
            marked <strong>Not Scored</strong>.
          </p>

          <p>
            ClimateCapital keeps those records for source history and
            transparency, but does not treat them as selectable projects in a
            Funding Plan.
          </p>

          <div className="reconciliation-line">
            <strong>136 PRB source rows</strong>
            <span aria-hidden="true">→</span>
            <span>106 projects</span>
            <span>23 program buckets</span>
            <span>4 program allocations</span>
            <span>3 Not Scored</span>
          </div>
        </section>

        <section aria-labelledby="priority-method-heading">
          <p className="eyebrow">Official project priority</p>
          <h2 id="priority-method-heading">What is Funding Priority?</h2>

          <p>
            Each governed project has an official{' '}
            <strong>PRB Grand Total</strong> from the City&apos;s scoring
            process.
          </p>

          <p>
            In ClimateCapital, we call this score{' '}
            <strong>Funding Priority</strong>.
          </p>

          <p>
            A higher Funding Priority means that the project received a higher
            overall PRB score. Projects with the same score share the same
            rank.
          </p>

          <aside className="information-callout">
            <strong>What the rank means</strong>
            <span>
              Funding Priority helps determine which projects are considered
              first in a Funding Plan. It does not predict which projects the
              City will ultimately choose.
            </span>
          </aside>

          <h3>What goes into Funding Priority?</h3>

          <div className="method-table-wrapper">
            <table className="method-table">
              <thead>
                <tr>
                  <th scope="col">PRB component</th>
                  <th scope="col">Maximum points</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Strategic Alignment</td>
                  <td>8</td>
                </tr>
                <tr>
                  <td>Critical Asset</td>
                  <td>8</td>
                </tr>
                <tr>
                  <td>Community Consideration</td>
                  <td>20</td>
                </tr>
                <tr>
                  <td>Efficiency</td>
                  <td>20</td>
                </tr>
                <tr>
                  <td>Timeliness &amp; Readiness</td>
                  <td>24</td>
                </tr>
                <tr>
                  <td>Climate Resilience</td>
                  <td>20</td>
                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <th scope="row">Maximum total</th>
                  <td>100</td>
                </tr>
              </tfoot>
            </table>
          </div>

          <p>
            ClimateCapital uses the official project scores as governed. It
            does <strong>not</strong> create new weights, change component
            scores, calculate score-per-dollar, or invent additional
            analytical tiebreakers.
          </p>

          <p className="methodology-note">
            <strong>Methodology note:</strong> Funding Priority is used as an{' '}
            <strong>ordinal priority measure</strong>. It tells us which
            projects rank higher or lower, but ClimateCapital does not assume
            that the numerical difference between two scores measures how much
            more valuable one project is than another.
          </p>
        </section>

        <section aria-labelledby="plan-method-heading">
          <p className="eyebrow">Funding Plan workflow</p>
          <h2 id="plan-method-heading">How is a Funding Plan built?</h2>

          <p className="information-lead">
            <strong>
              You choose the Available Project Budget. ClimateCapital then
              works through projects from higher to lower Funding Priority.
            </strong>
          </p>

          <ol className="method-steps">
            <li>
              <strong>Set a budget</strong>
              <span>
                Choose one of the reference budgets or enter your own
                Available Project Budget.
              </span>
            </li>

            <li>
              <strong>Start with the highest Funding Priority</strong>
              <span>
                ClimateCapital considers higher-priority project groups first.
              </span>
            </li>

            <li>
              <strong>Fund a complete priority group when it fits</strong>
              <span>
                Projects are treated as full funding requests rather than
                partially funded pieces.
              </span>
            </li>

            <li>
              <strong>
                Stop when an equal-priority group cannot be resolved
                automatically
              </strong>
              <span>
                If several projects have the same Funding Priority but there
                is not enough budget for all of them, ClimateCapital does not
                invent a preference among equally ranked projects.
              </span>
            </li>

            <li>
              <strong>Ask the analyst</strong>
              <span>
                When more than one valid choice remains, the application
                requests Analyst Resolution.
              </span>
            </li>
          </ol>

          <aside className="information-callout">
            <strong>Not a score-maximizing optimizer</strong>
            <span>
              ClimateCapital does not search for the combination that spends
              the most money or produces the highest sum of scores. It follows
              the Funding Priority rules and asks for human judgment when
              those rules cannot determine a unique choice.
            </span>
          </aside>

          <p className="methodology-note">
            <strong>Technical methodology:</strong>{' '}
            Priority-Constrained Analyst-Governed Portfolio Construction.
          </p>
        </section>

        <section aria-labelledby="remaining-budget-heading">
          <p className="eyebrow">Budget interpretation</p>
          <h2 id="remaining-budget-heading">
            Why can money remain after a Funding Plan is complete?
          </h2>

          <p>
            Projects have specific full funding requests, so they do not
            always fit perfectly into the remaining budget.
          </p>

          <p>
            A completed Funding Plan can therefore have{' '}
            <strong>Remaining Budget</strong>.
          </p>

          <p>
            ClimateCapital does not choose lower-priority or cheaper projects
            simply to spend every available dollar.
          </p>
        </section>

        <section aria-labelledby="benchmark-method-heading">
          <p className="eyebrow">Historical comparison</p>
          <h2 id="benchmark-method-heading">
            What is the Historical Benchmark?
          </h2>

          <p>
            The <strong>Historical Benchmark</strong> shows what was included
            in the City&apos;s{' '}
            <strong>January 21, 2026 Initial Draft Recommendation</strong>.
          </p>

          <p>
            The full historical recommendation was{' '}
            <strong>$700 million</strong>.
          </p>

          <div
            className="benchmark-reconciliation"
            aria-label="Historical recommendation reconciliation"
          >
            <div>
              <strong>$700M</strong>
              <span>Full January recommendation</span>
            </div>

            <span className="benchmark-operator" aria-hidden="true">
              =
            </span>

            <div>
              <strong>$332M</strong>
              <span>
                Recommendation associated with projects in ClimateCapital&apos;s
                106-project universe
              </span>
            </div>

            <span className="benchmark-operator" aria-hidden="true">
              +
            </span>

            <div>
              <strong>$368M</strong>
              <span>Recommendation outside that project-level universe</span>
            </div>
          </div>

          <p>
            This distinction matters. A ClimateCapital Funding Plan with a
            $700M Available Project Budget should <strong>not</strong> be
            expected to reproduce the City&apos;s $700M historical
            recommendation, because $368M of that historical package was
            outside the 106-project project-level universe modeled here.
          </p>

          <p>
            The Historical Benchmark is used only for retrospective
            comparison. It never changes Funding Priority, project ranks,
            Funding Plan construction, or Analyst Resolution.
          </p>
        </section>

        <section aria-labelledby="geometry-method-heading">
          <p className="eyebrow">Location evidence</p>
          <h2 id="geometry-method-heading">What about project locations?</h2>

          <p>
            Project-level mapped locations are not available in the governed
            January 21 dataset used by ClimateCapital.
          </p>

          <p>
            Rather than guessing where a project belongs, ClimateCapital
            leaves its location unmarked.
          </p>

          <p>
            <strong>
              0 of 106 projects currently have governed project geometry in
              this historical dataset.
            </strong>
          </p>

          <p>
            Projects remain fully available for evidence review and Funding
            Plan analysis.
          </p>

          <p>
            ClimateCapital does not create coordinates from project names,
            convert Council Districts into project locations, or add estimated
            map pins.
          </p>
        </section>

        <section aria-labelledby="gemini-method-heading">
          <p className="eyebrow">AI assistance</p>
          <h2 id="gemini-method-heading">How does Gemini help?</h2>

          <p>
            <strong>
              Gemini helps turn complex project and funding information into
              explanations that are easier to understand.
            </strong>
          </p>

          <p>
            You can ask Gemini questions about a project, its Funding Priority,
            the six PRB components, a Funding Plan result, an unresolved
            boundary, or the Historical Benchmark.
          </p>

          <div className="gemini-role-grid">
            <article>
              <h3>Gemini can help explain</h3>
              <ul>
                <li>Why a project has its Funding Priority.</li>
                <li>
                  Which PRB components contribute to a project&apos;s score.
                </li>
                <li>
                  Why a Funding Plan stopped at a particular priority tier.
                </li>
                <li>Why Analyst Resolution is required.</li>
                <li>What Remaining Budget means.</li>
                <li>
                  How a current Funding Plan differs from the Historical
                  Benchmark.
                </li>
              </ul>
            </article>

            <article>
              <h3>Gemini does not</h3>
              <ul>
                <li>Change project scores or ranks.</li>
                <li>Select which project should receive funding.</li>
                <li>Create new project evidence.</li>
                <li>Invent project locations.</li>
                <li>Override Analyst Resolution.</li>
                <li>Change the deterministic Funding Plan calculation.</li>
              </ul>
            </article>
          </div>

          <aside className="information-callout information-callout-primary">
            <strong>
              ClimateCapital calculates the Funding Plan; Gemini helps you
              understand it.
            </strong>
          </aside>
        </section>

        <section aria-labelledby="sources-heading">
          <p className="eyebrow">Data provenance</p>
          <h2 id="sources-heading">Where does the information come from?</h2>

          <p>
            ClimateCapital is built from City of Austin source material
            associated with the 2026 Bond Program, including project requests,
            Project Review Board scoring, and the January 21, 2026 Initial
            Draft Recommendation.
          </p>

          <p>
            ClimateCapital keeps project names, funding requests, scores,
            source departments, and available source references connected to
            the records they came from.
          </p>

          <p>
            When different source versions contain a known difference,
            ClimateCapital preserves that information rather than silently
            replacing it.
          </p>

          <dl className="dataset-summary">
            <div>
              <dt>Historical snapshot</dt>
              <dd>January 21, 2026</dd>
            </div>
            <div>
              <dt>PRB source rows reviewed</dt>
              <dd>136</dd>
            </div>
            <div>
              <dt>Governed project universe</dt>
              <dd>106</dd>
            </div>
            <div>
              <dt>Governed project request total</dt>
              <dd>$1.97352B</dd>
            </div>
          </dl>
        </section>
      </div>
    </main>
  )
}