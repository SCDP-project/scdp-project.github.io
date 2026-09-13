(() => {
  "use strict";

  const videos = [...document.querySelectorAll(".demo-video")];
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const toggle = document.querySelector(".playback-toggle");
  const visible = new Set();
  const manuallyPaused = new WeakSet();
  const automaticPauses = new WeakSet();
  let autoplayPaused =
    reducedMotion.matches || Boolean(navigator.connection?.saveData);

  const tryPlay = (video) => {
    const play = video.play();
    if (play)
      play.catch(() => {
        /* Native controls remain available if autoplay is blocked. */
      });
  };
  const pauseAutomatically = (video) => {
    if (!video.paused) {
      automaticPauses.add(video);
      video.pause();
    }
  };
  const syncPlayback = () => {
    videos.forEach((video) => {
      if (
        visible.has(video) &&
        !autoplayPaused &&
        !document.hidden &&
        !manuallyPaused.has(video)
      ) {
        tryPlay(video);
      } else {
        pauseAutomatically(video);
      }
    });
    toggle.setAttribute("aria-pressed", String(autoplayPaused));
    toggle.querySelector(".playback-label").textContent = autoplayPaused
      ? "Enable autoplay"
      : "Pause autoplay";
    toggle.querySelector(".playback-symbol").textContent = autoplayPaused
      ? "▷"
      : "Ⅱ";
  };

  videos.forEach((video) => {
    video.muted = true;
    video.addEventListener("pause", () => {
      if (automaticPauses.has(video)) automaticPauses.delete(video);
      else if (!video.ended && video.readyState > 0) manuallyPaused.add(video);
    });
    video.addEventListener("play", () => manuallyPaused.delete(video));
    video.addEventListener("error", () => {
      let message = video.parentElement.querySelector(".media-error");
      if (!message) {
        message = document.createElement("p");
        message.className = "media-error";
        message.setAttribute("role", "status");
        video.parentElement.append(message);
      }
      message.replaceChildren("Unable to play this video. ");
      const link = document.createElement("a");
      link.href = video.querySelector("source").src;
      link.textContent = "Open the video directly.";
      message.append(link);
    });
    video.addEventListener("loadeddata", () =>
      video.parentElement.querySelector(".media-error")?.remove(),
    );
  });

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(({ target, isIntersecting, intersectionRatio }) => {
          if (isIntersecting && intersectionRatio >= 0.2) visible.add(target);
          else visible.delete(target);
        });
        syncPlayback();
      },
      { threshold: [0, 0.2] },
    );
    videos.forEach((video) => observer.observe(video));
  } else {
    // With no visibility observer, use the native controls instead of loading every video.
    autoplayPaused = true;
    toggle.hidden = true;
  }
  syncPlayback();
  document.addEventListener("visibilitychange", syncPlayback);
  toggle.addEventListener("click", () => {
    autoplayPaused = !autoplayPaused;
    if (!autoplayPaused)
      videos.forEach((video) => manuallyPaused.delete(video));
    syncPlayback();
  });
  reducedMotion.addEventListener("change", (event) => {
    autoplayPaused = event.matches;
    syncPlayback();
  });

  const copyButton = document.querySelector("#copy-bibtex");
  copyButton.addEventListener("click", async () => {
    const code = document.querySelector("#bibtex-code");
    const status = document.querySelector("#copy-status");
    try {
      await navigator.clipboard.writeText(code.textContent.trim());
      copyButton.querySelector("span").textContent = "Copied!";
      status.textContent = "BibTeX copied to clipboard.";
      setTimeout(() => {
        copyButton.querySelector("span").textContent = "Copy BibTeX";
      }, 2000);
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = "Citation selected. Press Ctrl+C or ⌘C to copy.";
    }
  });
})();
