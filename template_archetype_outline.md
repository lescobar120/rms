# Template Registry & Archetype Data Structure Outline

## Phase 1: Additional Templates & Content Registry

### Recommended Additional Templates

#### 1. Earnings Preview/Preview Note Template
**Purpose**: Pre-earnings analysis and expectations setting

**Data Captured**:
- Consensus estimates vs analyst estimates
- Key metrics to watch (revenue, margins, guidance)
- Scenario analysis (bull/base/bear cases)
- Historical earnings surprise patterns
- Key questions for management
- Risk factors and catalysts

#### 2. Sector/Thematic Research Template
**Purpose**: Broader market views and sector rotation narratives

**Data Captured**:
- Sector outlook and positioning
- Relative valuations across sector
- Top picks and conviction levels
- Macro themes and catalysts
- Comparative analysis tables
- Investment timeline and catalysts

#### 3. Quick Update/Flash Note Template
**Purpose**: Rapid response to news, events, or price movements

**Data Captured**:
- Event description and immediate impact
- Revised estimates or target prices
- Recommendation changes
- Brief rationale and next steps
- Updated risk assessment

#### 4. Initiation Coverage Template
**Purpose**: First-time coverage establishment

**Data Captured**:
- Complete investment thesis
- Detailed financial model introduction
- Peer comparison and positioning
- Risk assessment framework
- Coverage universe context
- Long-term outlook and catalysts

#### 5. Meeting/Management Interaction Template
**Purpose**: Post-meeting insights and takeaways

**Data Captured**:
- Meeting participants and format
- Key discussion topics and insights
- Management guidance changes
- Competitive intelligence
- Follow-up actions and timeline

### Template Registry Infrastructure Requirements

#### Template Management System
- Template versioning and approval workflow
- Dynamic field mapping for different content types
- Conditional logic for archetype-specific variations
- Content validation rules and quality checks

#### Data Integration Points
- CDE field mapping for each template type
- Note metadata standardization across templates
- Tag taxonomy alignment with template categories
- Publishing schedule coordination

#### Content Generation Engine
- Template selection logic based on triggers
- Data injection points for market/fundamental data
- Archetype behavior influence on template choice
- Content depth variation based on analyst profile

---

## Market & Fundamental Data Architecture

### Raw Data Structure Approach

**Core Philosophy**: Store normalized raw data with calculated derived metrics, not pre-calculated scenarios. This provides maximum flexibility for archetype behavior simulation.

### Data Architecture Pattern

**Star Schema Foundation**:
- **Fact Tables**: Price movements, earnings events, estimate revisions
- **Dimension Tables**: Securities, time periods, analysts, sectors
- **Bridge Tables**: Security relationships, analyst coverage, sector classifications

### Core Data Entities

#### 1. Security Master Data
- Security identifiers and classifications
- Sector/industry hierarchies
- Market cap, float, trading characteristics
- Corporate structure and relationships

#### 2. Market Data Time Series
- Daily/intraday price and volume data
- Volatility metrics and correlation matrices
- Technical indicators and momentum measures
- Liquidity and trading pattern data

#### 3. Fundamental Data Repository
- Historical financial statements (quarterly/annual)
- Consensus estimates and revisions history
- Analyst recommendation changes
- Guidance and management commentary

#### 4. Event Calendar Data
- Earnings announcement dates and times
- Corporate actions and ex-dates
- Conference and presentation schedules
- Regulatory filing deadlines

#### 5. News & Information Events
- News categorization and sentiment
- Regulatory announcements
- Industry reports and surveys
- Management changes and strategic announcements

### Calculated Metrics Layer

#### Performance Attribution
- Forward-looking return calculations (1d, 1w, 1m, 3m, 6m, 1y)
- Risk-adjusted performance metrics
- Sector and market relative performance
- Volatility and correlation dynamics

#### Accuracy Measurement Framework
- Estimate accuracy vs actual results
- Target price achievement tracking
- Recommendation performance attribution
- Timing analysis for revisions and changes

#### Event Impact Analysis
- Pre/post event price movements
- Earnings surprise impact quantification
- News event reaction patterns
- Sector rotation timing measurements

### Data Access Patterns

#### Real-Time Query Layer
- Current market state and positioning
- Recent performance and momentum
- Immediate event impact assessment
- Live consensus and estimate data

#### Historical Analysis Engine
- Lookback performance calculations
- Pattern recognition and similarity matching
- Seasonal and cyclical trend analysis
- Long-term accuracy and timing patterns

#### Scenario Generation Framework
- Forward-looking event simulation
- Market regime change modeling
- Sector rotation probability assessment
- Individual security opportunity identification

---

## Analyst Archetype Data Structures

### Behavioral Component Architecture

**Individual Behavior Classes** (Composable Components):

#### 1. AccuracyBehavior
- Base accuracy distribution parameters
- Confidence interval characteristics
- Sector-specific accuracy variations
- Learning and adaptation rates

#### 2. TimingBehavior
- Response delay distributions
- Event sensitivity thresholds
- Consensus relationship parameters
- Publication frequency patterns

#### 3. CoverageBehavior
- Universe size preferences
- Sector concentration limits
- Idea capacity constraints
- Research depth vs breadth trade-offs

#### 4. BiasBehavior
- Overconfidence/underconfidence tendencies
- Anchoring preferences (price, consensus, prior views)
- Loss aversion coefficients
- Confirmation bias strengths

#### 5. ProductivityBehavior
- Research volume targets
- Idea progression speed preferences
- Content depth variation patterns
- Workload management styles

### Archetype Composition Framework

#### Base Analyst Class Structure
- Core identification (name, firm, start date)
- Coverage universe definition
- Performance tracking state
- Current workload and capacity

#### Archetype Configuration
- Behavior component composition
- Parameter weighting and interaction rules
- Performance target ranges
- Constraint definitions

#### Dynamic State Management
- Current performance streaks
- Recent activity patterns
- Confidence level adjustments
- Workload and attention allocation

### Behavior Parameterization Approach

#### Flexible Parameter System
- Range-based definitions (min/max with distributions)
- Context-dependent adjustments
- Performance feedback influence
- Market regime modifications

#### Example: Timing Behavior Parameters
- Base response delay: 2-48 hours (normal distribution)
- Event magnitude sensitivity: 0.3-0.8 scaling factor
- Consensus deviation threshold: 5-15% trigger levels
- Publication frequency: 0.5-3.0x sector average

#### Behavior Interaction Rules
- Cross-behavior influence coefficients
- Constraint violation handling
- Performance pressure responses
- Market stress adaptations

### Archetype Inheritance Strategy

**Composition over Inheritance**: Rather than inheriting from base archetype classes, use component composition for maximum flexibility.

#### Archetype Definition Structure
```yaml
Archetype:
  name: "The Oracle"
  behaviors:
    accuracy: AccuracyBehavior(params...)
    timing: TimingBehavior(params...)
    coverage: CoverageBehavior(params...)
    bias: BiasBehavior(params...)
    productivity: ProductivityBehavior(params...)
  interaction_rules: {...}
  constraints: {...}
  performance_targets: {...}
```

### State Tracking Requirements

#### Performance State
- Rolling accuracy metrics
- Recent recommendation performance
- Current streak status (hot/cold)
- Confidence level adjustments

#### Activity State
- Active ideas and their stages
- Recent publication history
- Current workload assessment
- Attention allocation

#### Market Context State
- Sector performance relative to analyst coverage
- Recent market regime characteristics
- Peer analyst activity levels
- Competitive positioning

### Archetype Instantiation Process

1. **Template Loading**: Base archetype configuration
2. **Parameter Randomization**: Within defined ranges for uniqueness
3. **Historical Calibration**: Adjust parameters based on assigned historical period
4. **State Initialization**: Set starting performance and activity levels
5. **Validation**: Ensure parameter consistency and constraint compliance

---

## Implementation Considerations

### Template Registry Development Priority

1. **Core Company Model Integration** (Current)
2. **Earnings Preview Template** (High Impact for demos)
3. **Quick Update Template** (High frequency, easy to automate)
4. **Sector Research Template** (Medium complexity, good narrative value)
5. **Meeting Notes Template** (Lower priority, specific use cases)

### Data Architecture Development Approach

#### Phase 1: Core Infrastructure
- Security master data structure
- Basic market data time series
- Simple event calendar integration

#### Phase 2: Calculated Metrics
- Performance attribution engine
- Accuracy measurement framework
- Basic event impact analysis

#### Phase 3: Advanced Analytics
- Pattern recognition systems
- Scenario generation capabilities
- Complex behavior interaction modeling

### Archetype System Complexity Management

#### Start Simple
- Begin with 2-3 basic behavior types
- Focus on clear parameter definitions
- Implement basic state tracking

#### Scale Incrementally
- Add complexity through composition
- Introduce behavior interactions gradually
- Validate each component before integration

#### Maintain Flexibility
- Design for easy parameter tuning
- Enable runtime behavior modification
- Support A/B testing of different approaches

This structure provides the foundation for a sophisticated yet manageable simulation system that can grow in complexity while maintaining clarity and performance.