module.exports = {
  ci: {
    collect: {
      staticDistDir: "./",
      numberOfRuns: 3
    },

    // Baseline phase: collect and upload reports without enforcing score thresholds.
    assert: {
      assertions: {}
    },

    upload: {
      target: "temporary-public-storage"
    }
  }
};
