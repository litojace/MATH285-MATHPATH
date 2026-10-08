import {Link} from 'react-router-dom';
export function NotFoundPage(){return <section className="page container empty"><span className="eyebrow red">404</span><h1>This path does not exist.</h1><p>Try the topic search or return to the course map.</p><Link className="button primary" to="/courses">Browse courses</Link></section>}
