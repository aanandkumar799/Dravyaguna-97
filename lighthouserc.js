module.exports = {
  ci: {
    collect: {
      staticDistDir: "./",
      numberOfRuns: 3
    },

    assert: {
      preset: "lighthouse:recommended"
    },

    upload: {
      target: "temporary-public-storage"
    }
  }
};
