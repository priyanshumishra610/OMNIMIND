import { test, expect } from '@playwright/test';

test.describe('Ascension UI E2E', () => {
  test('loads main cockpit and finds all core components', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('canvas')).toBeVisible(); // AmbientLayer
    await expect(page.locator('text=E1')).toBeVisible(); // NeuralMesh node
    await expect(page.locator('text=Start Session')).toBeVisible(); // MindTimeline event
    await expect(page.locator('text=Energy:')).toBeVisible(); // BioSimPanel
    await expect(page.locator('text=Chain-of-Thought')).toBeVisible(); // MorpheusConsole tab
    await expect(page.locator('text=WebSearch')).toBeVisible(); // PluginChamber
  });
}); 