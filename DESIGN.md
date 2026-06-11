---
name: Modern AI Intelligence
colors:
  surface: '#031427'
  surface-dim: '#031427'
  surface-bright: '#2a3a4f'
  surface-container-lowest: '#000f21'
  surface-container-low: '#0b1c30'
  surface-container: '#102034'
  surface-container-high: '#1b2b3f'
  surface-container-highest: '#26364a'
  on-surface: '#d3e4fe'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#d3e4fe'
  inverse-on-surface: '#213145'
  outline: '#8c909f'
  outline-variant: '#424754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e6a'
  primary-container: '#4d8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#bec6e0'
  on-secondary: '#283044'
  secondary-container: '#3f465c'
  on-secondary-container: '#adb4ce'
  tertiary: '#ffb786'
  on-tertiary: '#502400'
  tertiary-container: '#df7412'
  on-tertiary-container: '#461f00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#dae2fd'
  secondary-fixed-dim: '#bec6e0'
  on-secondary-fixed: '#131b2e'
  on-secondary-fixed-variant: '#3f465c'
  tertiary-fixed: '#ffdcc6'
  tertiary-fixed-dim: '#ffb786'
  on-tertiary-fixed: '#311400'
  on-tertiary-fixed-variant: '#723600'
  background: '#031427'
  on-background: '#d3e4fe'
  surface-variant: '#26364a'
typography:
  display:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.01em
  code:
    fontFamily: jetbrainsMono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.6'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  sidebar-width: 280px
  max-content-width: 800px
  container-padding: 24px
  bubble-padding: 12px 16px
  gutter: 16px
---

## Brand & Style
The design system focuses on **Functional Minimalism**. It is designed to minimize cognitive load, allowing the user's conversation with AI to take center stage. The aesthetic is "Workplace Premium"—polished, reliable, and professional without unnecessary decoration. 

The interface leverages a high-contrast layout where information density is carefully managed. By utilizing generous whitespace and a restricted color palette, we evoke a sense of calm intelligence. The primary movement is **Corporate Modern**, leaning into precise geometry and subtle tonal shifts to indicate hierarchy.

## Colors
The palette is anchored by **Dark Slate (#0f172a)** for structural elements and **Primary Blue (#3b82f6)** for action-oriented highlights. 

- **Primary Blue:** Reserved for the User’s message bubbles, primary action buttons, and active states.
- **Secondary Slate:** Used for the sidebar and secondary navigation surfaces to provide clear containment.
- **Neutral Grays:** Utilized for secondary text, metadata, and subtle borders.
- **Dark Mode (Default):** Deep ink backgrounds (`#020617`) with slate surfaces.
- **Light Mode:** High-contrast white backgrounds with light gray (`#f1f5f9`) surfaces and slate text.

## Typography
This design system uses **Inter** for all UI elements to ensure maximum legibility and a systematic, utilitarian feel. For technical output or AI-generated code snippets, **JetBrains Mono** is used to provide a clear visual distinction.

The type scale is optimized for readability. Body-lg is the standard for chat bubbles to reduce eye strain during long reading sessions. Headlines are kept tight and bold to define section changes without consuming excessive vertical space.

## Layout & Spacing
The layout follows a **Fixed-Fluid model**:
- **Sidebar:** A fixed 280px navigation area on the left for history and account management. On mobile, this transforms into a hidden drawer.
- **Chat Feed:** A centered, fluid column with a maximum width of 800px. This ensures line lengths remain optimal for reading.
- **Spacing Rhythm:** Based on an 8px grid. Use 16px (2 units) for element grouping and 24px-32px (3-4 units) for sectional spacing.

Margins are consistent across the viewport to maintain a "frame" around the conversation.

## Elevation & Depth
Depth is communicated through **Tonal Layers** rather than heavy shadows. 

1. **Level 0 (Background):** The deepest layer (e.g., the main chat canvas).
2. **Level 1 (Surface):** Sidebar and secondary panels, slightly lighter or darker than the background to create contrast.
3. **Level 2 (Interaction):** Floating elements like the chat input bar use a subtle ambient shadow (10% opacity, 12px blur) to appear "closer" to the user, suggesting they are ready for input.

Borders are strictly **1px** and low-contrast, acting as subtle dividers rather than structural walls.

## Shapes
The shape language is **Rounded (Level 2)**. 
- **Standard UI (Buttons, Inputs):** 0.5rem (8px) radius.
- **Chat Bubbles:** 1rem (16px) for the outer corners, with a smaller 4px radius on the corner "tail" to indicate the speaker.
- **Containers:** Large cards or the sidebar use 1.5rem (24px) for a soft, modern container feel.

## Components
### Chat Bubbles
- **User:** Primary Blue background, white text. Aligned to the right. 
- **Assistant:** Slate surface (in dark mode) or Light Gray (in light mode). Aligned to the left. No heavy borders.

### Input Field
- **Structure:** A persistent text area at the bottom of the viewport. 
- **Styling:** 1px border (`#1e293b`). When focused, the border transitions to Primary Blue with a 2px outer glow.
- **Actions:** Icon buttons (attach, send) should be monochrome until hovered, then adopt the Primary Blue color.

### Sidebar (History)
- **Items:** List items with a hover state that uses a subtle background tint.
- **Active State:** A left-aligned 3px vertical "pill" indicator in Primary Blue.

### Buttons
- **Primary:** Solid Primary Blue with white text.
- **Secondary:** Ghost style with 1px slate borders and subtle hover fills.