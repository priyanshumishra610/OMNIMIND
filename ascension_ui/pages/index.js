import dynamic from 'next/dynamic';
import Head from 'next/head';
import AmbientLayer from '../components/AmbientLayer';
import NeuralMesh from '../components/NeuralMesh';
import EmotionPlasma from '../components/EmotionPlasma';
import MindTimeline from '../components/MindTimeline';
import BioSimPanel from '../components/BioSimPanel';
import MorpheusConsole from '../components/MorpheusConsole';
import PluginChamber from '../components/PluginChamber';

/**
 * OMNIMIND Cockpit Main Page
 * Cinematic, immersive AGI control room UI.
 */
export default function Home() {
  // Stub: mock emotion and biosim state
  const emotion = { stress: 0.3, focus: 0.7, curiosity: 0.5 };
  const biosim = { energy: 0.85, fatigue: 0.15, sleeping: false };
  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-ambient">
      <Head>
        <title>OMNIMIND Cockpit</title>
        <meta name="description" content="OMNIMIND Living Mind Cockpit" />
      </Head>
      <AmbientLayer />
      <main className="relative z-10 flex flex-col items-center justify-center min-h-screen p-6 gap-8">
        <div className="w-full flex flex-col md:flex-row gap-8 justify-between">
          <div className="flex-1 flex flex-col gap-8">
            <NeuralMesh />
            <EmotionPlasma emotion={emotion} />
          </div>
          <div className="flex-1 flex flex-col gap-8">
            <MindTimeline />
            <BioSimPanel state={biosim} />
          </div>
        </div>
        <div className="w-full flex flex-col md:flex-row gap-8 justify-between">
          <div className="flex-1">
            <MorpheusConsole />
          </div>
          <div className="flex-1">
            <PluginChamber />
          </div>
        </div>
      </main>
    </div>
  );
} 