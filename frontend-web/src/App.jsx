import './App.css';
import Card3D from './components/card/Card3D';
import Button3D from './components/button/Button3D';
import Button2D from './components/button/Button2D';
import Switch from './components/switch/Switch';
import ProgressBar from './components/progressBar/ProgressBar';

function App() {

  return (
    <>
      <Card3D display='grid'>
        Card 3D

        <Button2D> Button 2D </Button2D>
        <Button3D> Button 3D </Button3D>

        <Switch size={18}></Switch>

        <ProgressBar progress={30} color={"grey"}></ProgressBar>
      </Card3D>
    </>
  )
}

export default App
