module.exports = {
  ci: {
    collect: {
      staticDistDir: "./",
      numberOfRuns: 3
    },

    // Baseline phase: collect and upload reports without meaningful score thresholds.
    assert: {
      assertions: {
        "categories:performance": ["warn", { minScore: 0 }],
        "categories:accessibility": ["warn", { minScore: 0 }],
        "categories:best-practices": ["warn", { minScore: 0 }],
        "categories:seo": ["warn", { minScore: 0 }]
      }
    },

    upload: {
      target: "temporary-public-storage"
    }
  }
};
