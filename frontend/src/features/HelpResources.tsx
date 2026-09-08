export function HelpResources() {
  return (
    <main
      id="help-resources"
      className="main-content information-page"
    >
      <header className="information-hero">
        <p className="eyebrow">Using ClimateCapital</p>
        <h1>Help &amp; Resources</h1>

        <p className="information-lead">
          <strong>
            ClimateCapital helps you explore project evidence, build Funding
            Plans, understand historical outcomes, and use Gemini to make
            complex project information easier to understand.
          </strong>
        </p>
      </header>

      <div className="information-sections">
        <section aria-labelledby="quick-start-heading">
          <p className="eyebrow">Getting started</p>
          <h2 id="quick-start-heading">Quick Start</h2>

          <ol className="help-steps">
            <li>
              <strong>Explore projects</strong>
              <span>
                Open Explore to browse the governed 106-project universe.
                Search and filter projects, review their funding requests and
                Funding Priority, and open a project to see its six PRB
                scoring components and available source context.
              </span>
            </li>

            <li>
              <strong>Choose an Available Project Budget</strong>
              <span>
                Open Funding Plan and choose one of the reference budgets or
                enter your own. Reference presets only populate the budget.
                They do not reproduce historical project selections or impose
                historical category allocations.
              </span>
            </li>

            <li>
              <strong>Review the Funding Plan</strong>
              <span>
                ClimateCapital processes higher Funding Priority groups first
                and shows the projects selected by the deterministic Funding
                Plan evaluator.
              </span>
            </li>

            <li>
              <strong>Resolve a boundary when necessary</strong>
              <span>
                If equally ranked projects cannot all fit within the remaining
                budget and more than one valid choice remains, ClimateCapital
                asks for Analyst Resolution. This prevents the application
                from inventing an unsupported preference among equally ranked
                projects.
              </span>
            </li>

            <li>
              <strong>Explore the Historical Benchmark</strong>
              <span>
                Open Historical Benchmark to review the January 21, 2026
                Initial Draft Recommendation separately from the current
                Funding Plan.
              </span>
            </li>

            <li>
              <strong>Ask Gemini</strong>
              <span>
                Select Ask Gemini whenever you want help understanding the
                governed evidence or a Funding Plan result. Gemini explains
                the information; it does not make funding decisions.
              </span>
            </li>
          </ol>
        </section>

        <section aria-labelledby="questions-heading">
          <p className="eyebrow">Understanding the results</p>
          <h2 id="questions-heading">Common Questions</h2>

          <div className="faq-list">
            <details>
              <summary>
                Why didn&apos;t ClimateCapital spend the entire budget?
              </summary>
              <p>
                Projects have full funding requests and do not always fit
                perfectly into the available amount.
              </p>
              <p>
                ClimateCapital does not choose lower-priority or cheaper
                projects merely to spend every dollar. Remaining Budget can
                therefore be part of a valid completed Funding Plan.
              </p>
            </details>

            <details>
              <summary>
                Why is ClimateCapital asking me to choose between projects?
              </summary>
              <p>
                The projects may have the same official Funding Priority and
                there may not be enough money to fund the entire priority
                group.
              </p>
              <p>
                When more than one valid choice remains, ClimateCapital does
                not manufacture a tiebreaker. The choice requires Analyst
                Resolution.
              </p>
            </details>

            <details>
              <summary>
                Does a higher Funding Priority mean ClimateCapital recommends
                the project?
              </summary>
              <p>No.</p>
              <p>
                Funding Priority represents the project&apos;s official PRB
                Grand Total and determines the order in which projects are
                considered by the Funding Plan methodology.
              </p>
              <p>
                It is not a prediction or independent recommendation by
                ClimateCapital.
              </p>
            </details>

            <details>
              <summary>
                Does the Historical Benchmark determine my Funding Plan?
              </summary>
              <p>No.</p>
              <p>
                Historical recommendation information is retained only for
                retrospective comparison. It never enters project ranking,
                Funding Plan selection, or Analyst Resolution.
              </p>
            </details>

            <details>
              <summary>
                Why doesn&apos;t a $700M Funding Plan reproduce Austin&apos;s
                historical $700M recommendation?
              </summary>
              <p>
                Only $332M of the historical $700M recommendation was
                associated with projects represented in ClimateCapital&apos;s
                106-project universe.
              </p>
              <p>
                The remaining $368M was outside that project-level universe.
                The two $700M scenarios therefore represent different scopes.
              </p>
            </details>

            <details>
              <summary>
                Does Gemini decide which projects receive funding?
              </summary>
              <p>No.</p>
              <p>
                Gemini explains governed evidence and deterministic results.
                Project selection remains controlled by the Funding Plan
                methodology and explicit analyst decisions.
              </p>
            </details>

            <details>
              <summary>
                Can I ask Gemini which equal-priority project I should choose?
              </summary>
              <p>
                Gemini can explain the governed differences between the
                projects, but it will not choose one for you or invent a new
                tiebreaker.
              </p>
              <p>The final choice remains an analyst decision.</p>
            </details>

            <details>
              <summary>
                Why aren&apos;t project locations displayed on a map?
              </summary>
              <p>
                Governed project-level geometry is not available in the
                historical snapshot.
              </p>
              <p>ClimateCapital does not fabricate project locations.</p>
            </details>

            <details>
              <summary>What does Remaining Budget mean?</summary>
              <p>
                Remaining Budget is the portion of the Available Project
                Budget left after funding the full-request projects selected
                by the Funding Plan.
              </p>
              <p>It is not an optimization error.</p>
            </details>
          </div>
        </section>

        <section aria-labelledby="more-context-heading">
          <p className="eyebrow">Learn more</p>
          <h2 id="more-context-heading">Need more context?</h2>

          <p>
            Visit <strong>Data &amp; Methodology</strong> for details about
            the project universe, Project Review Board scoring, Funding
            Priority, Funding Plan construction, the Historical Benchmark,
            project-location limitations, and Gemini&apos;s role.
          </p>
        </section>

        <section aria-labelledby="official-resources-heading">
          <p className="eyebrow">Source material</p>
          <h2 id="official-resources-heading">Official City of Austin resources</h2>

          <p>
            ClimateCapital is based on City of Austin source material for the
            2026 Bond Program. Official City resources remain the authoritative
            source for the City&apos;s bond-development process and published
            recommendations.
          </p>

          <ul className="resource-list">
            <li>2026 Bond Development materials</li>
            <li>January 21, 2026 Initial Draft Recommendation</li>
            <li>Project Review Board scoring material</li>
          </ul>

          <p className="methodology-note">
            Official source links can be surfaced from governed project
            provenance where available. ClimateCapital should not invent or
            infer missing source references.
          </p>
        </section>
      </div>
    </main>
  )
}