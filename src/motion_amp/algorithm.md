# Scientific Specification: Real-Time Eulerian Motion Magnification

## 1. Problem Formulation
Motion amplification targets the visualization of subtle variations in intensity or position that are below the human visual threshold. Given a video sequence $I(x, y, t)$, we aim to produce an output $O(x, y, t)$ where movements in a specific frequency band $\omega \in [\omega_L, \omega_H]$ are magnified by a factor $\alpha$.

## 2. Eulerian Approximation
Following Wu et al. (2012), we use the Eulerian perspective, which observes changes at fixed spatial locations.
For a small displacement $\delta(t)$, the intensity can be approximated via Taylor expansion:
$$I(x + \delta(t), t) \approx I(x, 0) + \delta(t) \frac{\partial I}{\partial x}$$
The bandpassed signal $B(x, y, t)$ isolates the component related to $\delta(t)$. The magnified signal is:
$$O(x, y, t) = I(x, y, t) + \alpha \cdot B(x, y, t)$$

## 3. Real-Time Temporal Filtering (IIR)
To maintain real-time performance and minimize memory footprint (avoiding a frame buffer for FFT), we employ a First-Order IIR Bandpass Filter.

The bandpass filter is constructed as the difference between two Low-Pass Filters (LPF) or a direct second-order Butterworth IIR. For efficiency, we use two first-order LPFs:
$$y_{low}(t) = (1 - r_L) y_{low}(t-1) + r_L x(t)$$
$$y_{high}(t) = (1 - r_H) y_{high}(t-1) + r_H x(t)$$
Where $r = 1 - e^{-2\pi f_c / f_s}$.
The bandpassed signal: $B(t) = y_{high}(t) - y_{low}(t)$.

## 4. Spatial Decomposition (Laplacian Pyramid)
To prevent noise amplification and halos, we amplify different spatial frequencies differently.
- Linear EVM is applied to the levels of a Laplacian Pyramid.
- Since $\alpha$ is constrained by the wavelength of the movement to avoid artifacts (the "$\alpha$ limit"):
  $$(1+\alpha)\delta(t) < \frac{\lambda}{8}$$
  Large $\alpha$ can be used on low-frequency spatial bands (coarse levels), while small $\alpha$ should be used on high-frequency spatial bands (fine levels).

## 5. Algorithmic Constraints
- **Sampling Rate ($f_s$):** Must be constant. Variable FPS from the camera will jitter the filter response.
- **Normalization:** Temporal filtering should be performed in a linearized color space or after intensity normalization to decouple luminance from chrominance. YCrCb or LAB is preferred over RGB.
- **Complexity:** $O(N)$ per frame, where $N$ is the number of pixels. Pyramid construction is the bottleneck.

## 6. Optimization Strategy
- **Pre-allocation:** All buffers for the pyramid levels and IIR states must be pre-allocated to avoid GC overhead in Python.
- **Vectorization:** Use `np.multiply` and `np.add` in-place where possible.
- **Async IO:** Camera capture must run in a separate thread to ensure $f_s$ stability.
